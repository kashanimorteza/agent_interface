"""Core Data: shared configuration, validation, Instance resolution, routing, and normalization."""

import importlib
import json
import re
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from functools import cache
from pathlib import Path
from types import MappingProxyType, ModuleType
from typing import Any
from uuid import UUID

import yaml
from model.interface import entities
from sqlalchemy.orm import InstrumentedAttribute

from database.interface import (
    CommandResult,
    ConfigurationError,
    DatabaseInstance,
    DeclarationMismatchError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    InvalidInputError,
    Order,
    OrderDirection,
)

ROOT = Path(__file__).resolve().parents[3]
CONFIGURATION_FILE = ROOT / "config.yaml"
_KEY = re.compile(r"[a-z][a-z0-9_]*")
_INSTANCE_KEY = re.compile(r"[A-Za-z][A-Za-z0-9_]*")


@dataclass(frozen=True)
class EngineSettings:
    """One configured Engine."""

    key: str
    name: str
    driver: str
    parameters: Mapping[str, Any]


@dataclass(frozen=True)
class InstanceSettings:
    """One complete configured Instance."""

    key: str
    name: str
    active: bool
    engine: str
    host: str | None
    port: int | None
    database: str
    username: str | None
    password: str | None = field(repr=False)
    options: Mapping[str, Any]


@dataclass(frozen=True)
class Configuration:
    """The validated Database Configuration."""

    engines: Mapping[str, EngineSettings]
    instances: Mapping[str, InstanceSettings]
    default_instance: str
    storage_root: str
    filter_combination: FilterCombination
    default_limit: int
    default_order: tuple[str, OrderDirection]
    initial_data: tuple[tuple[type[Any], tuple[Mapping[str, Any], ...]], ...]


class _StrictLoader(yaml.SafeLoader):
    """A YAML loader that refuses a repeated key instead of keeping the last one."""

    def construct_mapping(
        self, node: yaml.MappingNode, deep: bool = False
    ) -> dict[Any, Any]:
        keys = [self.construct_object(key, deep=deep) for key, _ in node.value]
        repeated = sorted({str(key) for key in keys if keys.count(key) > 1})
        if repeated:
            raise ConfigurationError(f"The configuration repeats the keys {repeated}.")
        return super().construct_mapping(node, deep)


def _mapping(value: Any, where: str, keys: set[str] | None = None) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or not all(isinstance(key, str) for key in value):
        raise ConfigurationError(f"{where} must be a mapping.")
    if keys is not None and set(value) != keys:
        raise ConfigurationError(
            f"{where} must hold exactly {sorted(keys)}; it holds {sorted(value)}."
        )
    return value


def _text(value: Any, where: str, *, nullable: bool = False) -> Any:
    if value is None and nullable:
        return None
    if not isinstance(value, str) or (not nullable and not value):
        raise ConfigurationError(
            f"{where} must be {'text or null' if nullable else 'non-empty text'}."
        )
    return value


def _integer(value: Any, where: str, *, nullable: bool = False) -> Any:
    if value is None and nullable:
        return None
    if isinstance(value, bool) or not isinstance(value, int):
        raise ConfigurationError(
            f"{where} must be {'an integer or null' if nullable else 'an integer'}."
        )
    return value


def _flag(value: Any, where: str) -> bool:
    if not isinstance(value, bool):
        raise ConfigurationError(f"{where} must be true or false.")
    return value


def _member[E: Enum](members: type[E], value: Any, where: str) -> E:
    try:
        return members[value]
    except KeyError, TypeError:
        raise ConfigurationError(
            f"{where} names no member of {members.__name__}."
        ) from None


def _engine(key: str, value: Any) -> EngineSettings:
    if not _KEY.fullmatch(key):
        raise ConfigurationError(f"The Engine key {key!r} is not a valid Engine name.")
    where = f"Engine {key}"
    data = _mapping(value, where, {"name", "driver", "parameters"})
    return EngineSettings(
        key=key,
        name=_text(data["name"], f"{where} name"),
        driver=_text(data["driver"], f"{where} driver"),
        parameters=MappingProxyType(
            dict(_mapping(data["parameters"], f"{where} parameters"))
        ),
    )


def _instance(key: str, value: Any) -> InstanceSettings:
    if not _INSTANCE_KEY.fullmatch(key):
        raise ConfigurationError(
            f"The Instance key {key!r} is not a valid Instance name."
        )
    where = f"Instance {key}"
    names = {
        "name",
        "active",
        "engine",
        "host",
        "port",
        "database",
        "username",
        "password",
        "options",
    }
    data = _mapping(value, where, names)
    return InstanceSettings(
        key=key,
        name=_text(data["name"], f"{where} name"),
        active=_flag(data["active"], f"{where} active"),
        engine=_text(data["engine"], f"{where} engine"),
        host=_text(data["host"], f"{where} host", nullable=True),
        port=_integer(data["port"], f"{where} port", nullable=True),
        database=_text(data["database"], f"{where} database"),
        username=_text(data["username"], f"{where} username", nullable=True),
        password=_text(data["password"], f"{where} password", nullable=True),
        options=MappingProxyType(dict(_mapping(data["options"], f"{where} options"))),
    )


def _initial_data(
    value: Any,
) -> tuple[tuple[type[Any], tuple[Mapping[str, Any], ...]], ...]:
    if not isinstance(value, list):
        raise ConfigurationError("initial_data must be a list.")
    known = {entity.__name__: entity for entity in entities}
    collection: list[tuple[type[Any], tuple[Mapping[str, Any], ...]]] = []
    for index, block in enumerate(value):
        data = _mapping(block, f"initial_data entry {index}", {"entity", "records"})
        name = _text(data["entity"], f"initial_data entry {index} entity")
        if name not in known:
            raise ConfigurationError(
                f"initial_data names {name!r}, which is not a Model Entity."
            )
        if any(entity is known[name] for entity, _ in collection):
            raise ConfigurationError(f"initial_data holds {name!r} more than once.")
        records = data["records"]
        if not isinstance(records, list):
            raise ConfigurationError(f"The records of {name} must be a list.")
        collection.append(
            (
                known[name],
                tuple(
                    MappingProxyType(dict(_mapping(record, f"A record of {name}")))
                    for record in records
                ),
            )
        )
    return tuple(collection)


def parse_configuration(document: Any) -> Configuration:
    """Validate a configuration document and return it as typed settings."""
    root = _mapping(
        document,
        "The configuration",
        {"engines", "instances", "settings", "initial_data"},
    )
    engines = {
        key: _engine(key, value)
        for key, value in _mapping(root["engines"], "engines").items()
    }
    instances = {
        key: _instance(key, value)
        for key, value in _mapping(root["instances"], "instances").items()
    }
    if len({key.upper() for key in instances}) != len(instances):
        raise ConfigurationError(
            "Two Instances share one DatabaseInstance member name."
        )
    if len({instance.name for instance in instances.values()}) != len(instances):
        raise ConfigurationError("Two Instances share one name.")
    for instance in instances.values():
        if instance.engine not in engines:
            raise ConfigurationError(
                f"Instance {instance.key} names an Engine that is not configured."
            )
    active = {key.upper() for key, instance in instances.items() if instance.active}
    if active != set(DatabaseInstance.__members__):
        raise ConfigurationError(
            "The active Instances differ from the DatabaseInstance members."
        )
    settings = _mapping(
        root["settings"],
        "settings",
        {"default_instance", "storage_root", "query", "lifecycle"},
    )
    default = _text(settings["default_instance"], "default_instance")
    if default not in instances or not instances[default].active:
        raise ConfigurationError(
            "default_instance must name an active configured Instance."
        )
    storage_root = _text(settings["storage_root"], "storage_root")
    if Path(storage_root).is_absolute() or ".." in Path(storage_root).parts:
        raise ConfigurationError(
            "storage_root must stay inside the Database Component."
        )
    query = _mapping(
        settings["query"],
        "query",
        {"filter_combination", "default_limit", "default_order"},
    )
    order = _mapping(query["default_order"], "default_order", {"field", "direction"})
    lifecycle = _mapping(settings["lifecycle"], "lifecycle", {"after_generation"})
    after = _mapping(
        lifecycle["after_generation"],
        "after_generation",
        {"enabled", "fail_on_error", "command"},
    )
    limit = _integer(query["default_limit"], "default_limit")
    _flag(after["enabled"], "after_generation enabled")
    _flag(after["fail_on_error"], "after_generation fail_on_error")
    if after["command"] != "prepare":
        raise ConfigurationError("after_generation command must be prepare.")
    return Configuration(
        engines=MappingProxyType(engines),
        instances=MappingProxyType(instances),
        default_instance=default,
        storage_root=storage_root,
        filter_combination=_member(
            FilterCombination, query["filter_combination"], "filter_combination"
        ),
        default_limit=limit if limit > 0 else -1,
        default_order=(
            _text(order["field"], "default_order field"),
            _member(OrderDirection, order["direction"], "default_order direction"),
        ),
        initial_data=_initial_data(root["initial_data"]),
    )


@cache
def configuration() -> Configuration:
    """Load and validate the Database Configuration the first time it is needed."""
    if not (ROOT / "pyproject.toml").is_file():
        raise ConfigurationError(
            "Database runs only from its own Component, not from an installed copy."
        )
    try:
        document = yaml.load(
            CONFIGURATION_FILE.read_text(encoding="utf-8"), Loader=_StrictLoader
        )
    except OSError, yaml.YAMLError:
        raise ConfigurationError("The Database Configuration cannot be read.") from None
    return parse_configuration(document)


def entity_type(entity: Any, *, instance: bool = False) -> type[Any]:
    """Return the Model Entity class a request names, refusing a name, a string, or any other object."""
    if instance:
        candidate = None if isinstance(entity, type) else type(entity)
    else:
        candidate = entity
    if not isinstance(candidate, type) or candidate not in entities:
        raise InvalidInputError(
            f"A request takes {'an Entity instance' if instance else 'an Entity class'} "
            "from the Model Entity Collection, never a name or another string."
        )
    return candidate


@dataclass(frozen=True)
class Connection:
    """The complete connection of one active Instance, handed by Core to its Engine unit."""

    key: str
    name: str
    engine: str
    driver: str
    parameters: Mapping[str, Any]
    host: str | None
    port: int | None
    database: str
    username: str | None
    password: str | None = field(repr=False)
    options: Mapping[str, Any]
    storage_root: Path


@dataclass(frozen=True)
class Query:
    """A validated query request with every default resolved."""

    filters: tuple[Filter, ...]
    combination: FilterCombination
    orders: tuple[Order, ...]
    limit: int


def instance_member(key: str) -> DatabaseInstance:
    """Return the DatabaseInstance member that publishes a configured Instance."""
    return DatabaseInstance[key.upper()]


def connection_for(instance: Any) -> Connection:
    """Resolve a request to its active Instance, or to the default Instance when none is given."""
    settings = configuration()
    if instance is None:
        key = settings.default_instance
    elif isinstance(instance, DatabaseInstance):
        key = next(
            (key for key in settings.instances if key.upper() == instance.name), ""
        )
        if key not in settings.instances:
            raise ConfigurationError("The selected Instance is not configured.")
    else:
        raise InvalidInputError(
            "An Instance is selected by a DatabaseInstance member, never by a string."
        )
    chosen = settings.instances[key]
    if not chosen.active:
        raise InactiveInstanceError(f"The Instance {chosen.name!r} is not active.")
    engine = settings.engines[chosen.engine]
    return Connection(
        key=key,
        name=chosen.name,
        engine=engine.key,
        driver=engine.driver,
        parameters=engine.parameters,
        host=chosen.host,
        port=chosen.port,
        database=chosen.database,
        username=chosen.username,
        password=chosen.password,
        options=chosen.options,
        storage_root=ROOT / settings.storage_root,
    )


def fields_of(entity: type[Any]) -> dict[str, Any]:
    """Return an Entity's physical Field names, each with its Declaration, in Declaration order."""
    return dict(zip(entity.model_fields, entity.declaration.fields, strict=True))


def physical_name(entity: type[Any], logical: str) -> str:
    """Return the physical Field name of an Entity's logical Field name."""
    return next(
        name for name, declared in fields_of(entity).items() if declared.name == logical
    )


_VALUE_TYPES: Mapping[str, Callable[[Any], bool]] = MappingProxyType(
    {
        "string": lambda value: isinstance(value, str),
        "integer": lambda value: isinstance(value, int) and not isinstance(value, bool),
        "float": lambda value: (
            isinstance(value, int | float) and not isinstance(value, bool)
        ),
        "decimal": lambda value: (
            isinstance(value, Decimal | int) and not isinstance(value, bool)
        ),
        "boolean": lambda value: isinstance(value, bool),
        "datetime": lambda value: (
            isinstance(value, datetime) and value.utcoffset() is not None
        ),
        "date": lambda value: (
            isinstance(value, date) and not isinstance(value, datetime)
        ),
        "time": lambda value: isinstance(value, time),
        "uuid": lambda value: isinstance(value, UUID),
    }
)
_TEXT_OPERATORS = frozenset(
    {FilterOperator.CONTAINS, FilterOperator.STARTS_WITH, FilterOperator.ENDS_WITH}
)
_NULL_OPERATORS = frozenset({FilterOperator.IS_NULL, FilterOperator.IS_NOT_NULL})
_NUMERIC_TYPES = frozenset({"integer", "float", "decimal"})


def field_reference(entity: type[Any], reference: Any) -> str:
    """Return the physical name of a Field reference of the Entity, refusing anything else."""
    if (
        not isinstance(reference, InstrumentedAttribute)
        or reference.class_ is not entity
        or reference.key not in entity.model_fields
    ):
        raise InvalidInputError(
            f"A Field reference of {entity.__name__} is required, such as {entity.__name__}.id."
        )
    return reference.key


def check_value(entity: type[Any], name: str, value: Any, *, what: str) -> None:
    """Refuse a value that is not compatible with the Field's declared Type."""
    declared = fields_of(entity)[name]
    if value is None or not _VALUE_TYPES[declared.type](value):
        raise InvalidInputError(
            f"{what} on {entity.__name__}.{name} needs a {declared.type} value."
        )


def _sequence(value: Any, what: str) -> tuple[Any, ...]:
    if value is None:
        return ()
    if not isinstance(value, list | tuple):
        raise InvalidInputError(f"{what} must be given as a list or tuple.")
    return tuple(value)


def _checked_filters(entity: type[Any], filters: Any) -> tuple[Filter, ...]:
    checked = _sequence(filters, "Filters")
    for condition in checked:
        if not isinstance(condition, Filter):
            raise InvalidInputError("Filters must be Filter values.")
        name = field_reference(entity, condition.field)
        if (
            condition.operator in _TEXT_OPERATORS
            and fields_of(entity)[name].type != "string"
        ):
            raise InvalidInputError(
                f"{condition.operator.name} needs a textual Field; {entity.__name__}.{name} is not."
            )
        if condition.operator in _NULL_OPERATORS:
            continue
        values = (
            condition.value
            if condition.operator is FilterOperator.IN
            else (condition.value,)
        )
        for value in values:
            check_value(entity, name, value, what=f"A {condition.operator.name} Filter")
    return checked


def _checked_orders(entity: type[Any], orders: Any) -> tuple[Order, ...]:
    checked = _sequence(orders, "Orders")
    for order in checked:
        if not isinstance(order, Order):
            raise InvalidInputError("Orders must be Order values.")
        field_reference(entity, order.field)
    return checked


def _checked_combination(combination: Any) -> FilterCombination:
    if combination is None:
        return configuration().filter_combination
    if not isinstance(combination, FilterCombination):
        raise InvalidInputError(
            "A combination is a FilterCombination member, never a string."
        )
    return combination


def resolve_filtering(entity: type[Any], filters: Any, combination: Any) -> Query:
    """Validate Filters and a combination and resolve the combination's default."""
    return Query(
        _checked_filters(entity, filters), _checked_combination(combination), (), -1
    )


def resolve_query(
    entity: type[Any], filters: Any, combination: Any, orders: Any, limit: Any
) -> Query:
    """Validate a list request and resolve its omitted combination, Orders, and limit from the configuration."""
    base = resolve_filtering(entity, filters, combination)
    checked = _checked_orders(entity, orders)
    if not checked:
        name, direction = configuration().default_order
        if name not in entity.model_fields:
            raise ConfigurationError(
                f"The default order Field {name!r} is not a Field of {entity.__name__}."
            )
        checked = (Order(getattr(entity, name), direction),)
    if limit is None:
        limit = configuration().default_limit
    elif isinstance(limit, bool) or not isinstance(limit, int):
        raise InvalidInputError("A limit must be an integer.")
    return Query(base.filters, base.combination, checked, limit if limit > 0 else -1)


def checked_aggregate_field(entity: type[Any], reference: Any, *, numeric: bool) -> str:
    """Validate the Field an aggregate works on: numeric for a total, comparable for a smallest or largest value."""
    name = field_reference(entity, reference)
    kind = fields_of(entity)[name].type
    if (numeric and kind not in _NUMERIC_TYPES) or (not numeric and kind == "boolean"):
        raise InvalidInputError(
            f"{entity.__name__}.{name} is not {'a numeric' if numeric else 'a comparable'} Field."
        )
    return name


def checked_identity(entity: type[Any], identity: Any) -> Any:
    """Validate a record identity against the Entity's Primary Key Type."""
    name = physical_name(entity, entity.declaration.primary_key)
    check_value(entity, name, identity, what="An identity")
    return identity


def checked_command(command: Any, parameters: Any) -> None:
    """Validate the native command text and its bound parameters."""
    if not isinstance(command, str) or not command.strip():
        raise InvalidInputError("A command must be non-empty text.")
    if parameters is not None and (
        isinstance(parameters, str | bytes)
        or not isinstance(parameters, Mapping | Sequence)
    ):
        raise InvalidInputError("Command parameters must be a mapping or a sequence.")


def engine_unit(connection: Connection) -> ModuleType:
    """Return the Engine unit that serves the Connection's Engine."""
    name = f"database.engine.{connection.engine}"
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError as error:
        if error.name != name:
            raise
        raise ConfigurationError(
            f"No Engine unit serves the Engine of Instance {connection.name!r}."
        ) from None


def route(connection: Connection, operation: str, *arguments: Any) -> Any:
    """Forward a validated request to its Engine unit with the Instance's connection and return the raw result."""
    return getattr(engine_unit(connection), operation)(connection, *arguments)


def _json_value(type_name: str, value: Any) -> Any:
    """Write a stored value as JSON; a value of the wrong kind is passed on unchanged so the Entity rejects it."""
    if type_name in ("datetime", "date", "time") and isinstance(
        value, datetime | date | time
    ):
        return value.isoformat()
    if type_name in ("decimal", "uuid") and isinstance(value, Decimal | UUID):
        return str(value)
    return value


def materialize(entity: type[Any], row: Mapping[str, Any]) -> Any:
    """Build an Entity from one stored row through the Entity's own reconstruction, never repairing the row."""
    try:
        document = {
            declared.name: _json_value(declared.type, row[name])
            for name, declared in fields_of(entity).items()
        }
        return entity.from_json(json.dumps(document, allow_nan=False))
    except KeyError, TypeError, ValueError:
        raise DeclarationMismatchError(
            f"A stored row of {entity.__name__} does not satisfy the Entity contract."
        ) from None


def _record(entity: type[Any], row: Mapping[str, Any] | None) -> Any:
    """Present a stored row as an Entity, or a missing record as None."""
    return None if row is None else materialize(entity, row)


def add(entity: Any, instance: Any) -> Any:
    """Store one new Entity on the selected Instance and return the stored Entity."""
    kind = entity_type(entity, instance=True)
    connection = connection_for(instance)
    return materialize(kind, route(connection, "add", entity))


def update(entity: Any, instance: Any) -> Any:
    """Replace the mutable Fields of the stored Entity the given one locates; None when none exists."""
    kind = entity_type(entity, instance=True)
    connection = connection_for(instance)
    return _record(kind, route(connection, "update", entity))


def list_entities(
    entity: Any,
    filters: Any,
    combination: Any,
    orders: Any,
    limit: Any,
    instance: Any,
) -> list[Any]:
    """Return the Entities that match, in the requested order and quantity."""
    kind = entity_type(entity)
    query = resolve_query(kind, filters, combination, orders, limit)
    connection = connection_for(instance)
    return [
        materialize(kind, row) for row in route(connection, "list_records", kind, query)
    ]


def get_by_id(entity: Any, identity: Any, instance: Any) -> Any:
    """Return the Entity with the identity, or None when none exists."""
    kind = entity_type(entity)
    checked_identity(kind, identity)
    connection = connection_for(instance)
    return _record(kind, route(connection, "get", kind, identity))


def delete_by_id(entity: Any, identity: Any, instance: Any) -> Any:
    """Remove the Entity with the identity and return it as it was; None when none exists."""
    kind = entity_type(entity)
    checked_identity(kind, identity)
    connection = connection_for(instance)
    return _record(kind, route(connection, "delete_record", kind, identity))


def set_active(entity: Any, identity: Any, active: bool, instance: Any) -> Any:
    """Enable or disable the Entity with the identity and return the final Entity; None when none exists."""
    kind = entity_type(entity)
    if "is_active" not in kind.model_fields:
        raise InvalidInputError(
            f"{kind.__name__} has no is_active Field to enable or disable."
        )
    checked_identity(kind, identity)
    connection = connection_for(instance)
    return _record(kind, route(connection, "set_active", kind, identity, active))


def count(entity: Any, filters: Any, combination: Any, instance: Any) -> int:
    """Return how many Entities match."""
    kind = entity_type(entity)
    query = resolve_filtering(kind, filters, combination)
    connection = connection_for(instance)
    return route(connection, "count", kind, query)


_ZERO: Mapping[str, Any] = MappingProxyType(
    {"integer": 0, "float": 0.0, "decimal": Decimal(0)}
)


def aggregate(
    function: str,
    entity: Any,
    field: Any,
    filters: Any,
    combination: Any,
    instance: Any,
) -> Any:
    """Return the total, smallest, or largest value of a Field; a total over nothing is zero, the others None."""
    kind = entity_type(entity)
    name = checked_aggregate_field(kind, field, numeric=function == "sum")
    query = resolve_filtering(kind, filters, combination)
    connection = connection_for(instance)
    value = route(connection, "aggregate", kind, function, name, query)
    if value is None and function == "sum":
        return _ZERO[fields_of(kind)[name].type]
    return value


def truncate(entity: Any, instance: Any) -> int:
    """Remove every record of one Entity and return how many were removed."""
    kind = entity_type(entity)
    connection = connection_for(instance)
    return route(connection, "truncate", kind)


def execute_command(command: Any, parameters: Any, instance: Any) -> CommandResult:
    """Run a native command on the selected Instance and report its outcome."""
    checked_command(command, parameters)
    connection = connection_for(instance)
    raw = route(connection, "execute", command, parameters)
    return CommandResult(
        rows=None if raw["rows"] is None else tuple(raw["rows"]),
        affected=raw["affected"],
        columns=None if raw["columns"] is None else tuple(raw["columns"]),
        success=raw["success"],
        message=raw["message"],
        instance=instance_member(connection.key),
    )
