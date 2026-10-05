import importlib
import json
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from pathlib import Path
from types import MappingProxyType, ModuleType
from typing import Any, cast

import yaml
from model.interface import entities
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import InstrumentedAttribute

COMPONENT_ROOT = Path(__file__).resolve().parents[2]
CONFIGURATION_FILE = COMPONENT_ROOT / "config.yaml"


class DatabaseError(Exception):
    pass


class ConfigurationError(DatabaseError):
    pass


class InactiveInstanceError(DatabaseError):
    pass


class InvalidInputError(DatabaseError):
    pass


class DeclarationMismatchError(DatabaseError):
    pass


class ConnectionFailureError(DatabaseError):
    pass


class ExecutionError(DatabaseError):
    pass


class LifecycleError(DatabaseError):
    pass


class FilterOperator(Enum):
    EQUALS = "EQUALS"
    NOT_EQUALS = "NOT_EQUALS"
    GREATER_THAN = "GREATER_THAN"
    GREATER_OR_EQUAL = "GREATER_OR_EQUAL"
    LESS_THAN = "LESS_THAN"
    LESS_OR_EQUAL = "LESS_OR_EQUAL"
    IN = "IN"
    CONTAINS = "CONTAINS"
    STARTS_WITH = "STARTS_WITH"
    ENDS_WITH = "ENDS_WITH"
    IS_NULL = "IS_NULL"
    IS_NOT_NULL = "IS_NOT_NULL"


class FilterCombination(Enum):
    AND = "AND"
    OR = "OR"


class OrderDirection(Enum):
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"


@dataclass(frozen=True)
class EngineSettings:
    key: str
    name: str
    driver: str
    parameters: dict[str, Any]


@dataclass(frozen=True)
class InstanceSettings:
    key: str
    name: str
    active: bool
    engine: str
    host: str | None
    port: int | None
    database: str | None
    username: str | None
    password: str | None
    options: dict[str, Any]


@dataclass(frozen=True)
class Settings:
    engines: dict[str, EngineSettings]
    instances: dict[str, InstanceSettings]
    default_instance: str
    storage_root: str
    filter_combination: FilterCombination
    default_limit: int
    default_order_field: str
    default_order_direction: OrderDirection
    after_generation_enabled: bool
    after_generation_fail_on_error: bool
    initial_data: list[dict[str, Any]]


_INSTANCE_FIELDS = ("name", "active", "engine", "host", "port", "database", "username", "password", "options")


def _fail(message: str) -> ConfigurationError:
    return ConfigurationError(f"Invalid configuration: {message}")


def _mapping(value: Any, where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise _fail(f"{where} must be a mapping")
    return value


def _enumeration[E: Enum](enumeration: type[E], name: Any, where: str) -> E:
    if not isinstance(name, str) or name not in enumeration.__members__:
        raise _fail(f"{where} names an unknown {enumeration.__name__} member")
    return enumeration[name]


def load_configuration(path: Path = CONFIGURATION_FILE) -> Settings:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError, yaml.YAMLError:
        raise _fail("the configuration cannot be read") from None
    raw = _mapping(raw, "the configuration")
    missing = [section for section in ("engines", "instances", "settings", "initial_data") if section not in raw]
    if missing:
        raise _fail(f"missing section {', '.join(missing)}")

    engines: dict[str, EngineSettings] = {}
    for key, entry in _mapping(raw["engines"], "engines").items():
        entry = _mapping(entry, f"engine {key}")
        if not all(isinstance(entry.get(field), str) and entry[field] for field in ("name", "driver")):
            raise _fail(f"engine {key} needs a name and a driver")
        engines[key] = EngineSettings(
            key, entry["name"], entry["driver"], _mapping(entry.get("parameters"), f"engine {key} parameters")
        )

    instances: dict[str, InstanceSettings] = {}
    normalized: set[str] = set()
    names: set[str] = set()
    for key, entry in _mapping(raw["instances"], "instances").items():
        entry = _mapping(entry, f"instance {key}")
        if set(entry) != set(_INSTANCE_FIELDS):
            raise _fail(f"instance {key} must define exactly {', '.join(_INSTANCE_FIELDS)}")
        if not isinstance(entry["name"], str) or not entry["name"] or not isinstance(entry["active"], bool):
            raise _fail(f"instance {key} needs a name and an active state")
        if entry["engine"] not in engines:
            raise _fail(f"instance {key} names an unknown engine")
        if key.upper() in normalized or entry["name"] in names:
            raise _fail(f"instance {key} duplicates another instance's identity")
        normalized.add(key.upper())
        names.add(entry["name"])
        instances[key] = InstanceSettings(
            key=key,
            name=entry["name"],
            active=entry["active"],
            engine=entry["engine"],
            host=entry["host"],
            port=entry["port"],
            database=entry["database"],
            username=entry["username"],
            password=entry["password"],
            options=_mapping(entry["options"], f"instance {key} options"),
        )
    for instance in instances.values():
        if not instance.active:
            continue
        required = engines[instance.engine].parameters.get("required_connection", [])
        absent = [field for field in required if getattr(instance, field) in (None, "")]
        if absent:
            raise _fail(f"active instance {instance.key} lacks required connection values: {', '.join(absent)}")

    settings = _mapping(raw["settings"], "settings")
    default = settings.get("default_instance")
    if default not in instances or not instances[default].active:
        raise _fail("the default instance must name an active instance")
    storage_root = settings.get("storage_root")
    if not isinstance(storage_root, str) or not storage_root:
        raise _fail("settings need a storage root")
    query = _mapping(settings.get("query"), "settings query")
    limit = query.get("default_limit")
    if isinstance(limit, bool) or not isinstance(limit, int):
        raise _fail("the default limit must be an integer")
    order = _mapping(query.get("default_order"), "the default order")
    if not isinstance(order.get("field"), str) or not order["field"]:
        raise _fail("the default order needs a field")
    after = _mapping(
        _mapping(settings.get("lifecycle"), "settings lifecycle").get("after_generation"), "after_generation"
    )
    if (
        not isinstance(after.get("enabled"), bool)
        or not isinstance(after.get("fail_on_error"), bool)
        or after.get("command") != "prepare"
    ):
        raise _fail("after_generation needs enabled, fail_on_error and the command prepare")

    initial = raw["initial_data"]
    if not isinstance(initial, list) or not all(
        isinstance(item, dict)
        and isinstance(item.get("entity"), str)
        and isinstance(item.get("records"), list)
        and all(isinstance(r, dict) for r in item["records"])
        for item in initial
    ):
        raise _fail("initial_data must list entities with their records")

    return Settings(
        engines=engines,
        instances=instances,
        default_instance=default,
        storage_root=storage_root,
        filter_combination=_enumeration(FilterCombination, query.get("filter_combination"), "the filter combination"),
        default_limit=limit if limit > 0 else -1,
        default_order_field=order["field"],
        default_order_direction=_enumeration(OrderDirection, order.get("direction"), "the default order direction"),
        after_generation_enabled=after["enabled"],
        after_generation_fail_on_error=after["fail_on_error"],
        initial_data=initial,
    )


SETTINGS = load_configuration()

DatabaseInstance = cast(
    type[Enum],
    Enum(
        "DatabaseInstance",
        {key.upper(): key.upper() for key, instance in SETTINGS.instances.items() if instance.active},
    ),
)

ENGINES_IN_USE = frozenset(instance.engine for instance in SETTINGS.instances.values() if instance.active)


def engine_unit(engine_key: str) -> ModuleType:
    if engine_key not in ENGINES_IN_USE:
        raise ConfigurationError(f"No Engine implementation exists for Engine {engine_key}")
    try:
        return importlib.import_module(f"database.engine.{engine_key}")
    except ModuleNotFoundError:
        raise ConfigurationError(
            f"The Engine implementation for Engine {engine_key} has not been generated; generate Database again"
        ) from None


def resolve_storage_path(instance: InstanceSettings, settings: Settings = SETTINGS) -> Path:
    root = (COMPONENT_ROOT / settings.storage_root).resolve()
    name = instance.database or ""
    if not root.is_relative_to(COMPONENT_ROOT.resolve()) or root == COMPONENT_ROOT.resolve():
        raise ConfigurationError(f"The storage root of instance {instance.key} is outside the Database Component")
    location = (root / name).resolve()
    if not name or Path(name).is_absolute() or location == root or not location.is_relative_to(root):
        raise ConfigurationError(f"The database location of instance {instance.key} escapes the Database storage")
    return location


_TYPE_CHECKS: dict[str, Any] = {
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "float": lambda v: isinstance(v, float),
    "decimal": lambda v: isinstance(v, Decimal),
    "boolean": lambda v: isinstance(v, bool),
    "string": lambda v: isinstance(v, str),
    "datetime": lambda v: isinstance(v, datetime) and v.tzinfo is not None,
}
_ORDERED_TYPES = frozenset({"integer", "float", "decimal", "string", "datetime"})
_TEXT_OPERATORS = frozenset({FilterOperator.CONTAINS, FilterOperator.STARTS_WITH, FilterOperator.ENDS_WITH})
_RANGE_OPERATORS = frozenset(
    {
        FilterOperator.GREATER_THAN,
        FilterOperator.GREATER_OR_EQUAL,
        FilterOperator.LESS_THAN,
        FilterOperator.LESS_OR_EQUAL,
    }
)
_NULL_OPERATORS = frozenset({FilterOperator.IS_NULL, FilterOperator.IS_NOT_NULL})


def field_reference(field: Any) -> tuple[Any, str, str]:
    """Return the Entity class, Field name and declared Type of a Field reference."""
    if not isinstance(field, InstrumentedAttribute):
        raise InvalidInputError("A Field must be given as a Field reference of an Entity, never as a string")
    entity = field.class_
    declaration = getattr(entity, "declaration", None)
    declared = {item.name: item for item in declaration.fields} if declaration is not None else {}
    if field.key not in declared:
        raise InvalidInputError("The Field reference does not belong to a Model Entity")
    return entity, field.key, declared[field.key].type


def check_value(field_type: str, operator: FilterOperator, value: Any) -> None:
    if operator in _NULL_OPERATORS:
        if value is not None:
            raise InvalidInputError(f"The operator {operator.name} takes no value")
        return
    if operator in _TEXT_OPERATORS and field_type != "string":
        raise InvalidInputError(f"The operator {operator.name} requires a textual Field")
    if operator in _RANGE_OPERATORS and field_type not in _ORDERED_TYPES:
        raise InvalidInputError(f"The operator {operator.name} requires an ordered Field")
    values = value if operator is FilterOperator.IN else (value,)
    if operator is FilterOperator.IN and (not isinstance(value, (tuple, list, set, frozenset))):
        raise InvalidInputError("The operator IN requires a collection of values")
    if any(v is None or not _TYPE_CHECKS[field_type](v) for v in values):
        raise InvalidInputError(f"The value is not compatible with a Field of Type {field_type}")


@dataclass(frozen=True)
class Filter:
    field: Any
    operator: FilterOperator
    value: Any = None

    def __post_init__(self) -> None:
        _, _, field_type = field_reference(self.field)
        if not isinstance(self.operator, FilterOperator):
            raise InvalidInputError("The operator must be a FilterOperator member, never a string")
        check_value(field_type, self.operator, self.value)
        if self.operator is FilterOperator.IN:
            object.__setattr__(self, "value", tuple(self.value))


@dataclass(frozen=True)
class Order:
    field: Any
    direction: OrderDirection = OrderDirection.ASCENDING

    def __post_init__(self) -> None:
        field_reference(self.field)
        if not isinstance(self.direction, OrderDirection):
            raise InvalidInputError("The direction must be an OrderDirection member, never a string")


@dataclass(frozen=True)
class CommandResult:
    rows: tuple[Mapping[str, Any], ...] | None
    affected: int | None
    columns: tuple[str, ...] | None
    success: bool
    message: str
    instance: Any

    def __post_init__(self) -> None:
        if self.rows is not None:
            object.__setattr__(self, "rows", tuple(MappingProxyType(dict(row)) for row in self.rows))
        if self.columns is not None:
            object.__setattr__(self, "columns", tuple(self.columns))


@dataclass(frozen=True)
class LifecycleResult:
    command: str
    instance: Any
    success: bool
    affected: int | None
    message: str


@dataclass(frozen=True)
class SelectedInstance:
    member: Any
    settings: InstanceSettings
    engine: EngineSettings
    unit: ModuleType


def select_instance(instance: Any = None) -> SelectedInstance:
    if instance is None:
        key = SETTINGS.default_instance
    elif isinstance(instance, DatabaseInstance):
        key = next((k for k in SETTINGS.instances if k.upper() == instance.name), instance.name)
    else:
        raise InvalidInputError("The Instance must be a DatabaseInstance member, never a string")
    settings = SETTINGS.instances.get(key)
    if settings is None:
        raise ConfigurationError(f"Instance {key} is not configured")
    if not settings.active:
        raise InactiveInstanceError(f"Instance {key} is not active")
    return SelectedInstance(
        DatabaseInstance[key.upper()], settings, SETTINGS.engines[settings.engine], engine_unit(settings.engine)
    )


@dataclass(frozen=True)
class Query:
    filters: tuple[Filter, ...]
    combination: FilterCombination
    orders: tuple[Order, ...]
    limit: int


def check_entity_class(entity: Any) -> Any:
    if not isinstance(entity, type) or entity not in entities:
        raise InvalidInputError("An Entity class imported from Model is required, never a name")
    return entity


def check_entity_instance(entity: Any) -> Any:
    if isinstance(entity, type) or type(entity) not in entities:
        raise InvalidInputError("An Entity instance created from a Model Entity is required, never a name")
    return entity


def check_id(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise InvalidInputError("An id must be an integer")
    return value


def check_field(entity: Any, field: Any, kinds: frozenset[str] | None = None) -> tuple[str, str]:
    owner, name, field_type = field_reference(field)
    if owner is not entity:
        raise InvalidInputError("The Field reference belongs to another Entity than the one given")
    if kinds is not None and field_type not in kinds:
        raise InvalidInputError(f"A Field of Type {field_type} cannot be used here")
    return name, field_type


NUMERIC_TYPES = frozenset({"integer", "float", "decimal"})
COMPARABLE_TYPES = _ORDERED_TYPES


def resolve_query(
    entity: Any,
    filters: Sequence[Filter] | None = None,
    combination: FilterCombination | None = None,
    orders: Sequence[Order] | None = None,
    limit: int | None = None,
    *,
    listing: bool = False,
) -> Query:
    check_entity_class(entity)
    given = () if filters is None else tuple(filters)
    for item in given:
        if not isinstance(item, Filter):
            raise InvalidInputError("Filters must be Filter values")
        check_field(entity, item.field)
    if combination is not None and not isinstance(combination, FilterCombination):
        raise InvalidInputError("The combination must be a FilterCombination member, never a string")
    resolved_orders: tuple[Order, ...] = ()
    resolved_limit = -1
    if listing:
        supplied = () if orders is None else tuple(orders)
        for item in supplied:
            if not isinstance(item, Order):
                raise InvalidInputError("Orders must be Order values")
            check_field(entity, item.field)
        if supplied:
            resolved_orders = supplied
        else:
            default_field = getattr(entity, SETTINGS.default_order_field, None)
            check_field(entity, default_field)
            resolved_orders = (Order(default_field, SETTINGS.default_order_direction),)
        if limit is None:
            resolved_limit = SETTINGS.default_limit
        elif isinstance(limit, bool) or not isinstance(limit, int):
            raise InvalidInputError("The limit must be an integer")
        else:
            resolved_limit = limit if limit > 0 else -1
    return Query(given, combination or SETTINGS.filter_combination, resolved_orders, resolved_limit)


def _serializable(value: Any) -> Any:
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    return value


def entity_values(entity: Any) -> dict[str, Any]:
    return {item.name: getattr(entity, item.name) for item in entity.declaration.fields}


def materialize(entity: Any, row: Mapping[str, Any]) -> Any:
    names = [item.name for item in entity.declaration.fields]
    if set(row) != set(names):
        raise DeclarationMismatchError(
            f"A stored row of {entity.declaration.name} does not have the Fields of its Entity"
        )
    try:
        return entity.from_json(json.dumps({name: _serializable(row[name]) for name in names}))
    except ValueError:
        raise DeclarationMismatchError(
            f"A stored row of {entity.declaration.name} does not satisfy its Entity contract"
        ) from None


_HANDLES: dict[str, Any] = {}


def _handle(selected: SelectedInstance) -> Any:
    key = selected.settings.key
    if key not in _HANDLES:
        file_backed = selected.engine.parameters.get("storage_kind") == "file"
        storage = resolve_storage_path(selected.settings) if file_backed else None
        _HANDLES[key] = selected.unit.connect(selected.settings, selected.engine, storage)
    return _HANDLES[key]


def run[R](instance: Any, work: Callable[[ModuleType, Any], R]) -> R:
    selected = select_instance(instance)
    handle = _handle(selected)
    try:
        with selected.unit.transaction(handle) as connection:
            return work(selected.unit, connection)
    except SQLAlchemyError as error:
        detail = str(getattr(error, "orig", None) or type(error).__name__)
        raise ExecutionError(f"The request failed on Instance {selected.settings.key}: {detail}") from None


def add(entity: Any, instance: Any = None) -> Any:
    check_entity_instance(entity)
    if entity.id is not None:
        raise InvalidInputError("Add requires a new Entity whose id is still pending")
    model = type(entity)
    return run(instance, lambda unit, cx: materialize(model, unit.add(cx, model, entity_values(entity))))


def update(entity: Any, instance: Any = None) -> Any:
    check_entity_instance(entity)
    if entity.id is None:
        raise InvalidInputError("Update requires an Entity whose id locates the record")
    model = type(entity)

    def work(unit: ModuleType, cx: Any) -> Any:
        row = unit.update(cx, model, entity.id, entity_values(entity))
        return None if row is None else materialize(model, row)

    return run(instance, work)


def list_entities(
    entity: Any,
    filters: Sequence[Filter] | None = None,
    combination: FilterCombination | None = None,
    orders: Sequence[Order] | None = None,
    limit: int | None = None,
    instance: Any = None,
) -> list[Any]:
    query = resolve_query(entity, filters, combination, orders, limit, listing=True)
    return run(instance, lambda unit, cx: [materialize(entity, row) for row in unit.select(cx, entity, query)])


def _by_id(operation: str, entity: Any, id: Any, instance: Any) -> Any:
    check_entity_class(entity)
    check_id(id)

    def work(unit: ModuleType, cx: Any) -> Any:
        row = getattr(unit, operation)(cx, entity, id)
        return None if row is None else materialize(entity, row)

    return run(instance, work)


def get_by_id(entity: Any, id: Any, instance: Any = None) -> Any:
    return _by_id("get_by_id", entity, id, instance)


def delete(entity: Any, id: Any, instance: Any = None) -> Any:
    return _by_id("delete", entity, id, instance)


def enable(entity: Any, id: Any, instance: Any = None) -> Any:
    return _by_id("enable", entity, id, instance)


def disable(entity: Any, id: Any, instance: Any = None) -> Any:
    return _by_id("disable", entity, id, instance)


def count(
    entity: Any,
    filters: Sequence[Filter] | None = None,
    combination: FilterCombination | None = None,
    instance: Any = None,
) -> int:
    query = resolve_query(entity, filters, combination)
    return run(instance, lambda unit, cx: unit.count(cx, entity, query))


def _aggregate(
    operation: str,
    kinds: frozenset[str],
    entity: Any,
    field: Any,
    filters: Sequence[Filter] | None,
    combination: FilterCombination | None,
    instance: Any,
) -> Any:
    check_entity_class(entity)
    name, _ = check_field(entity, field, kinds)
    query = resolve_query(entity, filters, combination)
    return run(instance, lambda unit, cx: getattr(unit, operation)(cx, entity, name, query))


def total(entity: Any, field: Any, filters: Any = None, combination: Any = None, instance: Any = None) -> Any:
    return _aggregate("total", NUMERIC_TYPES, entity, field, filters, combination, instance)


def smallest(entity: Any, field: Any, filters: Any = None, combination: Any = None, instance: Any = None) -> Any:
    return _aggregate("smallest", COMPARABLE_TYPES, entity, field, filters, combination, instance)


def largest(entity: Any, field: Any, filters: Any = None, combination: Any = None, instance: Any = None) -> Any:
    return _aggregate("largest", COMPARABLE_TYPES, entity, field, filters, combination, instance)


def truncate(entity: Any, instance: Any = None) -> int:
    check_entity_class(entity)
    return run(instance, lambda unit, cx: unit.truncate(cx, entity))


def execute_command(command: Any, parameters: Any = None, instance: Any = None) -> CommandResult:
    if not isinstance(command, str) or not command.strip():
        raise InvalidInputError("A native command must be a non-empty string")
    if parameters is not None and (
        isinstance(parameters, str | bytes) or not isinstance(parameters, Mapping | Sequence)
    ):
        raise InvalidInputError("Command parameters must be a mapping or a sequence")
    member = select_instance(instance).member
    try:
        rows, affected, columns = run(instance, lambda unit, cx: unit.execute_command(cx, command, parameters))
    except ExecutionError as error:
        return CommandResult(None, None, None, False, str(error), member)
    return CommandResult(rows, affected, columns, True, "The command succeeded", member)


def report_failure[R](command: str, instance: Any, work: Callable[[], R]) -> R:
    key = select_instance(instance).settings.key
    try:
        return work()
    except DatabaseError as error:
        raise type(error)(f"{command} failed on Instance {key}: {error}") from None
