"""Core Data: shared contracts, validation, resolution, routing, and normalization for every public request."""

import importlib
import json
import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field as dataclass_field
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from pathlib import Path
from types import ModuleType
from typing import Any, Final, cast
from uuid import UUID

import yaml
from sqlalchemy.orm import QueryableAttribute
from sqlmodel import SQLModel


class DatabaseError(Exception):
    """Base of every Database error."""


class ConfigurationError(DatabaseError):
    """The configuration or the selected Instance is invalid."""


class InactiveInstanceError(DatabaseError):
    """An inactive Instance was selected."""


class InvalidInputError(DatabaseError):
    """A request carried invalid input or an invalid Field."""


class DeclarationMismatchError(DatabaseError):
    """An Entity Declaration and an existing Table or stored row are incompatible."""


class ConnectionFailureError(DatabaseError):
    """A connection to the selected Instance could not be established."""


class ExecutionError(DatabaseError):
    """The Engine failed to execute a request."""


class LifecycleError(DatabaseError):
    """A Lifecycle Command ended in an incomplete state."""


class FilterOperator(Enum):
    """The comparison operators a Filter may use."""

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
    """The ways several Filters combine."""

    AND = "AND"
    OR = "OR"


class OrderDirection(Enum):
    """The directions a result may be ordered in."""

    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"


def _require_field_reference(field: object) -> None:
    if not isinstance(field, QueryableAttribute):
        raise InvalidInputError(
            "A Field must be passed as the Entity's Field reference."
        )


@dataclass(frozen=True, eq=False)
class Filter:
    """An immutable condition: a Field reference, a comparison operator, and a value."""

    field: QueryableAttribute[Any]
    operator: FilterOperator
    value: object = None

    def __post_init__(self) -> None:
        _require_field_reference(self.field)
        if not isinstance(self.operator, FilterOperator):
            raise InvalidInputError(
                "A Filter operator must be a FilterOperator member."
            )
        if self.operator in (FilterOperator.IS_NULL, FilterOperator.IS_NOT_NULL):
            if self.value is not None:
                raise InvalidInputError(f"{self.operator.name} takes no value.")
        elif self.operator is FilterOperator.IN:
            if isinstance(self.value, str | bytes) or not isinstance(
                self.value, Iterable
            ):
                raise InvalidInputError("IN requires a collection of values.")
            object.__setattr__(self, "value", tuple(self.value))
        elif self.value is None:
            raise InvalidInputError(f"{self.operator.name} requires a value.")

    def _identity(self) -> tuple[object, ...]:
        return (self.field.class_, self.field.key, self.operator, self.value)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Filter) and self._identity() == other._identity()

    def __hash__(self) -> int:
        return hash(self._identity())


@dataclass(frozen=True, eq=False)
class Order:
    """An immutable ordering: a Field reference and a direction, ascending when none is given."""

    field: QueryableAttribute[Any]
    direction: OrderDirection = OrderDirection.ASCENDING

    def __post_init__(self) -> None:
        _require_field_reference(self.field)
        if not isinstance(self.direction, OrderDirection):
            raise InvalidInputError(
                "An Order direction must be an OrderDirection member."
            )

    def _identity(self) -> tuple[object, ...]:
        return (self.field.class_, self.field.key, self.direction)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Order) and self._identity() == other._identity()

    def __hash__(self) -> int:
        return hash(self._identity())


CONFIGURATION_PATH: Final = Path(__file__).resolve().parents[2] / "config.yaml"
_INSTANCE_PROPERTIES: Final = (
    "name",
    "active",
    "engine",
    "host",
    "port",
    "database",
    "username",
    "password",
    "options",
)
_CONNECTION_VALUES: Final = ("host", "port", "database", "username", "password")


@dataclass(frozen=True)
class EngineSpec:
    """One declared Engine and everything an Engine unit needs to connect and validate."""

    key: str
    name: str
    driver: str
    parameters: Mapping[str, Any]


@dataclass(frozen=True)
class InstanceSpec:
    """One complete, named database identity."""

    key: str
    name: str
    active: bool
    engine: str
    host: str | None
    port: int | None
    database: str
    username: str | None
    password: str | None = dataclass_field(repr=False)
    options: Mapping[str, Any] = dataclass_field(repr=False)


@dataclass(frozen=True)
class QueryDefaults:
    """Defaults applied to an omitted combination, Order set, or limit."""

    filter_combination: FilterCombination
    default_limit: int
    default_order_field: str
    default_order_direction: OrderDirection


@dataclass(frozen=True)
class AfterGeneration:
    """Whether and how generation prepares the default Instance."""

    enabled: bool
    fail_on_error: bool
    command: str


@dataclass(frozen=True)
class Settings:
    """Component-wide runtime settings."""

    default_instance: str
    storage_root: str
    query: QueryDefaults
    after_generation: AfterGeneration


@dataclass(frozen=True)
class InitialDataSet:
    """The configured Initial Data records of one Entity, in Target order."""

    entity: str
    records: tuple[Mapping[str, Any], ...]


@dataclass(frozen=True)
class Configuration:
    """The Database Configuration: the sole runtime source of Engines, Instances, Settings, and Initial Data."""

    engines: Mapping[str, EngineSpec]
    instances: Mapping[str, InstanceSpec]
    settings: Settings
    initial_data: tuple[InitialDataSet, ...]


class _UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that refuses a repeated mapping key instead of keeping the last."""

    def construct_mapping(
        self, node: yaml.MappingNode, deep: bool = False
    ) -> dict[Any, Any]:
        seen: set[object] = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in seen:
                raise ConfigurationError(
                    f"The Database Configuration repeats the key '{key}'."
                )
            seen.add(key)
        return super().construct_mapping(node, deep=deep)


def _read_configuration(path: Path) -> Mapping[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            raw = yaml.load(handle, Loader=_UniqueKeyLoader)
    except (OSError, yaml.YAMLError) as error:
        raise ConfigurationError(
            "The Database Configuration could not be read."
        ) from error
    if not isinstance(raw, dict):
        raise ConfigurationError("The Database Configuration must hold one mapping.")
    return raw


def _mapping(parent: Mapping[str, Any], key: str, where: str) -> Mapping[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        raise ConfigurationError(f"{where} must hold a mapping named '{key}'.")
    return value


def _text(parent: Mapping[str, Any], key: str, where: str) -> str:
    value = parent.get(key)
    if not isinstance(value, str) or not value:
        raise ConfigurationError(f"{where} must hold a non-empty text '{key}'.")
    return value


def _flag(parent: Mapping[str, Any], key: str, where: str) -> bool:
    value = parent.get(key)
    if not isinstance(value, bool):
        raise ConfigurationError(f"{where} must hold a true or false '{key}'.")
    return value


def member_name(key: str) -> str:
    """The public DatabaseInstance member name for an Instance key."""
    return re.sub(r"\W", "_", key).upper()


def _engine(key: str, raw: object) -> EngineSpec:
    where = f"Engine '{key}'"
    if not isinstance(raw, dict):
        raise ConfigurationError(f"{where} must be a mapping.")
    return EngineSpec(
        key,
        _text(raw, "name", where),
        _text(raw, "driver", where),
        dict(_mapping(raw, "parameters", where)),
    )


def _instance(key: str, raw: object, engines: Mapping[str, EngineSpec]) -> InstanceSpec:
    where = f"Instance '{key}'"
    if not isinstance(raw, dict):
        raise ConfigurationError(f"{where} must be a mapping.")
    missing = [name for name in _INSTANCE_PROPERTIES if name not in raw]
    if missing:
        raise ConfigurationError(f"{where} is incomplete: it lacks '{missing[0]}'.")
    engine = _text(raw, "engine", where)
    if engine not in engines:
        raise ConfigurationError(f"{where} names an Engine that is not declared.")
    port = raw["port"]
    if port is not None and (isinstance(port, bool) or not isinstance(port, int)):
        raise ConfigurationError(f"{where} must hold a whole-number or null 'port'.")
    for name in ("host", "username", "password"):
        if raw[name] is not None and not isinstance(raw[name], str):
            raise ConfigurationError(f"{where} must hold a text or null '{name}'.")
    if not isinstance(raw["options"], dict):
        raise ConfigurationError(f"{where} must hold a mapping 'options'.")
    spec = InstanceSpec(
        key,
        _text(raw, "name", where),
        _flag(raw, "active", where),
        engine,
        raw["host"],
        port,
        _text(raw, "database", where),
        raw["username"],
        raw["password"],
        dict(raw["options"]),
    )
    if spec.active:
        for name in engines[engine].parameters.get("required_parameters", ()):
            if name not in _CONNECTION_VALUES or getattr(spec, name) in (None, ""):
                raise ConfigurationError(
                    f"{where} lacks the connection value '{name}' its Engine requires."
                )
    return spec


def _resolve_member[M: Enum](enumeration: type[M], name: object, where: str) -> M:
    if not isinstance(name, str) or name not in enumeration.__members__:
        raise ConfigurationError(
            f"{where} names an unknown {enumeration.__name__} member."
        )
    return enumeration[name]


def _normalized_limit(value: object) -> int:
    if value is None:
        return -1
    if isinstance(value, bool) or not isinstance(value, int):
        raise ConfigurationError("The default limit must be a whole number.")
    return value if value > 0 else -1


def _settings(
    raw: Mapping[str, Any], instances: Mapping[str, InstanceSpec]
) -> Settings:
    where = "Settings"
    default_instance = _text(raw, "default_instance", where)
    chosen = instances.get(default_instance)
    if chosen is None or not chosen.active:
        raise ConfigurationError(
            "The default Instance must name an active declared Instance."
        )
    query = _mapping(raw, "query", where)
    order = _mapping(query, "default_order", "Query defaults")
    after = _mapping(
        _mapping(raw, "lifecycle", where), "after_generation", "Lifecycle settings"
    )
    command = _text(after, "command", "After-generation settings")
    if command != "prepare":
        raise ConfigurationError(
            "After-generation preparation must run the prepare command."
        )
    return Settings(
        default_instance,
        _text(raw, "storage_root", where),
        QueryDefaults(
            _resolve_member(
                FilterCombination,
                query.get("filter_combination"),
                "The default combination",
            ),
            _normalized_limit(query.get("default_limit")),
            _text(order, "field", "The default order"),
            _resolve_member(
                OrderDirection, order.get("direction"), "The default order direction"
            ),
        ),
        AfterGeneration(
            _flag(after, "enabled", "After-generation settings"),
            _flag(after, "fail_on_error", "After-generation settings"),
            command,
        ),
    )


def _initial_data(raw: object) -> tuple[InitialDataSet, ...]:
    if not isinstance(raw, list):
        raise ConfigurationError("Initial Data must be a list of Entity record sets.")
    sets: list[InitialDataSet] = []
    for entry in raw:
        if not isinstance(entry, dict) or not isinstance(entry.get("records"), list):
            raise ConfigurationError(
                "Every Initial Data entry must name an Entity and hold its records."
            )
        entity = _text(entry, "entity", "An Initial Data entry")
        if not all(isinstance(record, dict) for record in entry["records"]):
            raise ConfigurationError(
                f"Initial Data for '{entity}' must hold field mappings."
            )
        sets.append(
            InitialDataSet(entity, tuple(dict(record) for record in entry["records"]))
        )
    return tuple(sets)


def load_configuration(path: Path = CONFIGURATION_PATH) -> Configuration:
    """Read the generated configuration, and only it, validate it completely, and resolve its names.

    Nothing is written. Any defect fails the whole load before anything is returned.
    """
    raw = _read_configuration(path)
    engines = {
        key: _engine(key, value)
        for key, value in _mapping(raw, "engines", "The configuration").items()
    }
    instances = {
        key: _instance(key, value, engines)
        for key, value in _mapping(raw, "instances", "The configuration").items()
    }
    if len({member_name(key) for key in instances}) != len(instances):
        raise ConfigurationError("Two Instances share one public Instance member name.")
    if len({spec.name for spec in instances.values()}) != len(instances):
        raise ConfigurationError("Two Instances share one name.")
    settings = _settings(_mapping(raw, "settings", "The configuration"), instances)
    return Configuration(
        engines, instances, settings, _initial_data(raw.get("initial_data"))
    )


configuration: Final = load_configuration()


def build_instance_enumeration(source: Configuration) -> type[Enum]:
    """One member per active Instance, named for it, carrying no connection value."""
    names = {
        member_name(key): member_name(key)
        for key, spec in source.instances.items()
        if spec.active
    }
    return Enum("DatabaseInstance", names)


DatabaseInstance: Final = build_instance_enumeration(configuration)
_INSTANCE_KEYS: Final = {member_name(key): key for key in configuration.instances}


def instance_key(member: Enum) -> str:
    """The configuration key of the Instance a DatabaseInstance member stands for."""
    return _INSTANCE_KEYS[member.name]


@dataclass(frozen=True)
class CommandResult:
    """The result of a Database-wide Operation."""

    rows: tuple[Mapping[str, Any], ...] | None
    affected: int | None
    columns: tuple[str, ...] | None
    success: bool
    message: str
    instance: Enum


@dataclass(frozen=True)
class LifecycleResult:
    """The result of a Lifecycle Command."""

    command: str
    instance: Enum
    success: bool
    affected: int | None
    message: str


COMPONENT_ROOT: Final = CONFIGURATION_PATH.parent
ACTIVITY_FIELD: Final = "is_active"


def _model_entities() -> tuple[type[SQLModel], ...]:
    """The Model's Entity Collection, the only way the Database learns Entities."""
    try:
        from model.interface import entities
    except ImportError as error:
        raise DeclarationMismatchError(
            "The Model does not publish its Entity Collection."
        ) from error
    published: list[type[SQLModel]] = []
    for entity in entities:
        declaration = getattr(entity, "declaration", None)
        required = (
            "name",
            "fields",
            "primary_key",
            "relations",
            "unique_constraints",
            "indexes",
        )
        if (
            not isinstance(entity, type)
            or not hasattr(entity, "__table__")
            or declaration is None
            or not all(hasattr(declaration, name) for name in required)
        ):
            raise DeclarationMismatchError(
                f"The Model Entity '{getattr(entity, '__name__', 'unknown')}' does not publish a usable Declaration."
            )
        published.append(entity)
    return tuple(published)


entity_collection: Final = _model_entities()


def declaration_of(entity: type[SQLModel]) -> Any:
    """The Declaration an Entity publishes."""
    return entity.declaration  # pyright: ignore[reportAttributeAccessIssue]


def table_of(entity: type[SQLModel]) -> Any:
    """The Table the Entity's table model maps to."""
    return entity.__table__  # pyright: ignore[reportAttributeAccessIssue]


def entity_from_json(entity: type[SQLModel], text: str) -> SQLModel:
    """Build an Entity through its own public JSON Object reconstruction."""
    return entity.from_json(text)  # pyright: ignore[reportAttributeAccessIssue]


def require_imported(value: object, label: str) -> None:
    """Refuse text where an imported Entity, Field reference, or vocabulary member is required."""
    if isinstance(value, str):
        raise InvalidInputError(
            f"{label} must be passed as the imported value, never as text."
        )


def require_member[M: Enum](value: object, enumeration: type[M], label: str) -> M:
    """Return the vocabulary member, refusing text and any other value."""
    require_imported(value, label)
    if not isinstance(value, enumeration):
        raise InvalidInputError(f"{label} must be a {enumeration.__name__} member.")
    return value


def entity_class(entity: object) -> type[SQLModel]:
    """An Entity class of the Model's Entity Collection."""
    require_imported(entity, "An Entity")
    if not isinstance(entity, type) or entity not in entity_collection:
        raise InvalidInputError("An Entity must be an Entity class of the Model.")
    return entity


def entity_instance(entity: object) -> SQLModel:
    """An instance of an Entity of the Model's Entity Collection."""
    require_imported(entity, "An Entity")
    if isinstance(entity, type) or type(entity) not in entity_collection:
        raise InvalidInputError("An Entity instance of the Model is required.")
    return cast(SQLModel, entity)


def resolve_instance(instance: Enum | None) -> InstanceSpec:
    """The Instance a request runs on; a request for an unusable Instance fails before storage is touched."""
    if instance is None:
        return configuration.instances[configuration.settings.default_instance]
    require_imported(instance, "An Instance")
    if not isinstance(instance, Enum):
        raise InvalidInputError("An Instance must be a DatabaseInstance member.")
    if isinstance(instance, DatabaseInstance):
        return configuration.instances[instance_key(instance)]
    key = _INSTANCE_KEYS.get(instance.name)
    if key is None:
        raise ConfigurationError("The selected Instance is not a configured Instance.")
    if not configuration.instances[key].active:
        raise InactiveInstanceError(f"Instance '{key}' is not active.")
    raise InvalidInputError("An Instance must be a DatabaseInstance member.")


_VALUE_TYPES: Final[dict[str, tuple[type, ...]]] = {
    "string": (str,),
    "integer": (int,),
    "float": (int, float),
    "decimal": (Decimal, int),
    "boolean": (bool,),
    "datetime": (datetime,),
    "date": (date,),
    "time": (time,),
    "uuid": (UUID,),
}
_NUMERIC_TYPES: Final = ("integer", "float", "decimal")
_COMPARABLE_TYPES: Final = (*_NUMERIC_TYPES, "string", "datetime", "date", "time")
_TEXT_MATCHING: Final = (
    FilterOperator.CONTAINS,
    FilterOperator.STARTS_WITH,
    FilterOperator.ENDS_WITH,
)


def field_type(entity: type[SQLModel], field_reference: object) -> str:
    """The declared Type of a Field reference, which must be a Field of the given Entity."""
    require_imported(field_reference, "A Field")
    if (
        not isinstance(field_reference, QueryableAttribute)
        or field_reference.class_ is not entity
    ):
        raise InvalidInputError(
            f"A Field must be a Field of the Entity {entity.__name__}."
        )
    for declared in declaration_of(entity).fields:
        if declared.name == field_reference.key:
            return declared.type
    raise InvalidInputError(f"A Field must be a Field of the Entity {entity.__name__}.")


def _compatible(declared_type: str, value: object) -> bool:
    if isinstance(value, bool) and declared_type != "boolean":
        return False
    if declared_type == "date" and isinstance(value, datetime):
        return False
    if (
        declared_type == "datetime"
        and isinstance(value, datetime)
        and value.tzinfo is None
    ):
        return False
    return isinstance(value, _VALUE_TYPES[declared_type])


def validate_filters(
    entity: type[SQLModel], filters: Sequence[Filter] | None
) -> tuple[Filter, ...]:
    """Check every Filter against the Entity's own Fields and Types before any Instance is accessed."""
    checked: list[Filter] = []
    for condition in filters or ():
        if not isinstance(condition, Filter):
            raise InvalidInputError("Filters must be Filter values.")
        declared_type = field_type(entity, condition.field)
        operator = condition.operator
        if operator in _TEXT_MATCHING and declared_type != "string":
            raise InvalidInputError(f"{operator.name} requires a textual Field.")
        if operator in (FilterOperator.IS_NULL, FilterOperator.IS_NOT_NULL):
            pass
        else:
            values = (
                cast(Iterable[object], condition.value)
                if operator is FilterOperator.IN
                else (condition.value,)
            )
            if not all(_compatible(declared_type, value) for value in values):
                raise InvalidInputError(
                    f"The value of this {operator.name} Filter does not fit the Field's Type."
                )
        checked.append(condition)
    return tuple(checked)


def validate_orders(
    entity: type[SQLModel], orders: Sequence[Order]
) -> tuple[Order, ...]:
    """Check every Order against the Entity's own Fields before any Instance is accessed."""
    for ordering in orders:
        if not isinstance(ordering, Order):
            raise InvalidInputError("Orders must be Order values.")
        field_type(entity, ordering.field)
    return tuple(orders)


def validate_aggregate_field(
    entity: type[SQLModel], field_reference: object, *, numeric: bool
) -> str:
    """Check the Field of an aggregate: numeric for a total, comparable for the smallest and largest."""
    declared_type = field_type(entity, field_reference)
    if declared_type not in (_NUMERIC_TYPES if numeric else _COMPARABLE_TYPES):
        kind = "numeric" if numeric else "comparable"
        raise InvalidInputError(f"This aggregate requires a {kind} Field.")
    return declared_type


_ENGINE_KEY: Final = re.compile(r"[a-z][a-z0-9_]*")
_connections: Final[dict[str, Any]] = {}


ENGINE_CAPABILITIES: Final = (
    "ATOMIC_STRUCTURE_CHANGES",
    "connect",
    "add",
    "get",
    "select_rows",
    "update",
    "delete_by_id",
    "count",
    "aggregate",
    "truncate",
    "execute",
    "create_tables",
    "insert_missing",
)


def engine_unit(engine_key: str) -> ModuleType:
    """The Engine unit named for an Engine, which must implement every capability the Database routes to it.

    Units are reached by name at call time, never imported ahead of a request.
    """
    if not _ENGINE_KEY.fullmatch(engine_key):
        raise ConfigurationError("An Engine key must be a lower-case name.")
    try:
        unit = importlib.import_module(f"database.engine.{engine_key}")
    except ModuleNotFoundError:
        raise ConfigurationError(
            f"Engine '{engine_key}' has no implementation."
        ) from None
    if any(not hasattr(unit, name) for name in ENGINE_CAPABILITIES):
        raise ConfigurationError(
            f"Engine '{engine_key}' does not implement every required capability."
        )
    return unit


def connection_for(instance: InstanceSpec) -> tuple[ModuleType, Any]:
    """The Engine unit and the connection of an Instance, built the first time a request needs it."""
    engine = configuration.engines[instance.engine]
    unit = engine_unit(engine.key)
    handle = _connections.get(instance.key)
    if handle is None:
        file_backed = engine.parameters.get("storage", {}).get("kind") == "file"
        location = resolve_storage_location(instance) if file_backed else None
        handle = unit.connect(instance, engine, location)
        _connections[instance.key] = handle
    return unit, handle


def instance_member(instance: InstanceSpec) -> Enum:
    """The DatabaseInstance member of an active Instance."""
    return DatabaseInstance[member_name(instance.key)]


def _json_value(declared_type: str, value: object) -> object:
    if value is None:
        return None
    if declared_type == "decimal" and isinstance(value, Decimal):
        return format(value, "f")
    if declared_type in ("datetime", "date", "time") and isinstance(
        value, date | datetime | time
    ):
        return value.isoformat()
    if declared_type == "uuid":
        return str(value)
    return value


def materialize(entity: type[SQLModel], row: Mapping[str, Any]) -> SQLModel:
    """Build an Entity from one stored row through the Entity's own public construction.

    A row that does not satisfy the Entity's contract is an error; it is never repaired, coerced, or skipped.
    """
    declared = {item.name: item.type for item in declaration_of(entity).fields}
    try:
        values = {
            name: _json_value(declared.get(name, ""), value)
            for name, value in row.items()
        }
        return entity_from_json(entity, json.dumps(values))
    except ValueError, TypeError:
        raise DeclarationMismatchError(
            f"A stored {entity.__name__} row does not satisfy the Entity contract."
        ) from None


def stored_values(entity: SQLModel) -> dict[str, Any]:
    """The Field values of an Entity instance, in Declaration order, without a still-pending generated identity."""
    declaration = declaration_of(type(entity))
    values: dict[str, Any] = {}
    for declared in declaration.fields:
        value = getattr(entity, declared.name)
        if declared.value_generation == "auto_increment":
            if value is not None:
                raise InvalidInputError("A new Entity must not carry an identity.")
            continue
        values[declared.name] = value
    return values


def add(entity: SQLModel, instance: Enum | None = None) -> SQLModel:
    """Store one complete new Entity and return the stored Entity, including generated values."""
    new = entity_instance(entity)
    values = stored_values(new)
    spec = resolve_instance(instance)
    unit, handle = connection_for(spec)
    return materialize(type(new), unit.add(handle, type(new), values))


def _identity(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise InvalidInputError("An id must be a whole number.")
    return value


def get_by_id(
    entity: type[SQLModel], id: int, instance: Enum | None = None
) -> SQLModel | None:
    """The stored Entity with the given id, or null when there is none."""
    cls = entity_class(entity)
    identity = _identity(id)
    spec = resolve_instance(instance)
    unit, handle = connection_for(spec)
    row = unit.get(handle, cls, identity)
    return materialize(cls, row) if row is not None else None


def matching_rows(
    entity: type[SQLModel],
    filters: Sequence[Filter] | None = None,
    combination: FilterCombination | None = None,
    instance: Enum | None = None,
) -> list[dict[str, Any]]:
    """The stored rows the Filters select; every row when no Filter is given."""
    cls = entity_class(entity)
    checked = validate_filters(cls, filters)
    resolved = resolve_combination(combination)
    spec = resolve_instance(instance)
    unit, handle = connection_for(spec)
    return unit.select_rows(handle, cls, checked, resolved)


def list_entities(
    entity: type[SQLModel],
    filters: Sequence[Filter] | None = None,
    combination: FilterCombination | None = None,
    orders: Sequence[Order] | None = None,
    limit: int | None = None,
    instance: Enum | None = None,
) -> list[SQLModel]:
    """The stored Entities of the class that the Filters select, in the Orders' sequence and at most limit.

    Each is built through its own construction. Omitted inputs resolve to the configured defaults; a limit of zero
    or below means no limit.
    """
    cls = entity_class(entity)
    checked = validate_filters(cls, filters)
    resolved = resolve_combination(combination)
    ordering = validate_orders(cls, resolve_orders(cls, orders))
    cap = resolve_limit(limit)
    spec = resolve_instance(instance)
    unit, handle = connection_for(spec)
    return [
        materialize(cls, row)
        for row in unit.select_rows(handle, cls, checked, resolved, ordering, cap)
    ]


def update(entity: SQLModel, instance: Enum | None = None) -> SQLModel | None:
    """Replace every mutable Field of the stored record the Entity's id locates; null when there is none."""
    changed = entity_instance(entity)
    cls = type(changed)
    declaration = declaration_of(cls)
    identity = getattr(changed, declaration.primary_key)
    if identity is None:
        raise InvalidInputError(
            "An Entity to update must carry the id that locates its record."
        )
    values = {
        declared.name: getattr(changed, declared.name)
        for declared in declaration.fields
        if not declared.immutable and declared.value_generation is None
    }
    spec = resolve_instance(instance)
    unit, handle = connection_for(spec)
    row = unit.update(handle, cls, _identity(identity), values)
    return materialize(cls, row) if row is not None else None


def delete(
    entity: type[SQLModel], id: int, instance: Enum | None = None
) -> SQLModel | None:
    """Remove the record with the given id and return it as it was just before removal; null when there is none."""
    cls = entity_class(entity)
    identity = _identity(id)
    spec = resolve_instance(instance)
    unit, handle = connection_for(spec)
    row = unit.delete_by_id(handle, cls, identity)
    return materialize(cls, row) if row is not None else None


def _set_activity(
    entity: type[SQLModel], id: int, active: bool, instance: Enum | None
) -> SQLModel | None:
    cls = entity_class(entity)
    identity = _identity(id)
    spec = resolve_instance(instance)
    unit, handle = connection_for(spec)
    row = unit.update(handle, cls, identity, {ACTIVITY_FIELD: active})
    return materialize(cls, row) if row is not None else None


def enable(
    entity: type[SQLModel], id: int, instance: Enum | None = None
) -> SQLModel | None:
    """Set only the activity flag to active; the final Entity, also when it already was, or null when none exists."""
    return _set_activity(entity, id, True, instance)


def disable(
    entity: type[SQLModel], id: int, instance: Enum | None = None
) -> SQLModel | None:
    """Set only the activity flag to inactive; the final Entity, also when it already was, or null when none exists."""
    return _set_activity(entity, id, False, instance)


def count(
    entity: type[SQLModel],
    filters: Sequence[Filter] | None = None,
    combination: FilterCombination | None = None,
    instance: Enum | None = None,
) -> int:
    """The number of stored records the Filters select."""
    cls = entity_class(entity)
    checked = validate_filters(cls, filters)
    resolved = resolve_combination(combination)
    spec = resolve_instance(instance)
    unit, handle = connection_for(spec)
    return unit.count(handle, cls, checked, resolved)


def _aggregate(
    function: str,
    entity: type[SQLModel],
    field_reference: Any,
    filters: Sequence[Filter] | None,
    combination: FilterCombination | None,
    instance: Enum | None,
) -> Any:
    cls = entity_class(entity)
    validate_aggregate_field(cls, field_reference, numeric=function == "sum")
    checked = validate_filters(cls, filters)
    resolved = resolve_combination(combination)
    spec = resolve_instance(instance)
    unit, handle = connection_for(spec)
    return unit.aggregate(handle, cls, function, field_reference.key, checked, resolved)


def total(
    entity: type[SQLModel],
    field: object,
    filters: Sequence[Filter] | None = None,
    combination: FilterCombination | None = None,
    instance: Enum | None = None,
) -> Any:
    """The total of one numeric Field over the selected records, ignoring nulls; zero when nothing matches."""
    return _aggregate("sum", entity, field, filters, combination, instance)


def smallest(
    entity: type[SQLModel],
    field: object,
    filters: Sequence[Filter] | None = None,
    combination: FilterCombination | None = None,
    instance: Enum | None = None,
) -> Any:
    """The smallest value of one comparable Field over the selected records, ignoring nulls; null when none."""
    return _aggregate("min", entity, field, filters, combination, instance)


def largest(
    entity: type[SQLModel],
    field: object,
    filters: Sequence[Filter] | None = None,
    combination: FilterCombination | None = None,
    instance: Enum | None = None,
) -> Any:
    """The largest value of one comparable Field over the selected records, ignoring nulls; null when none."""
    return _aggregate("max", entity, field, filters, combination, instance)


def truncate(entity: type[SQLModel], instance: Enum | None = None) -> int:
    """Remove every record of the Entity, keep its Table, and return the number removed."""
    cls = entity_class(entity)
    spec = resolve_instance(instance)
    unit, handle = connection_for(spec)
    return unit.truncate(handle, cls)


def execute_command(
    command: str,
    parameters: Mapping[str, Any] | Sequence[Any] | None = None,
    instance: Enum | None = None,
) -> CommandResult:
    """Run one native command on the selected Instance."""
    if not isinstance(command, str) or not command.strip():
        raise InvalidInputError("A command must be non-empty text.")
    if isinstance(parameters, str | bytes) or not (
        parameters is None or isinstance(parameters, Mapping | Sequence)
    ):
        raise InvalidInputError("Command parameters must be a mapping or a sequence.")
    spec = resolve_instance(instance)
    unit, handle = connection_for(spec)
    rows, affected, columns = unit.execute(handle, command, parameters)
    return CommandResult(
        tuple(rows) if rows is not None else None,
        affected,
        tuple(columns) if columns is not None else None,
        True,
        "The command completed.",
        instance_member(spec),
    )


def resolve_combination(combination: FilterCombination | None) -> FilterCombination:
    """An omitted combination resolves to the configured default."""
    if combination is None:
        return configuration.settings.query.filter_combination
    return require_member(combination, FilterCombination, "A combination")


def resolve_limit(limit: int | None) -> int:
    """An omitted limit resolves to the configured default; zero or negative means no limit (-1)."""
    if limit is None:
        return configuration.settings.query.default_limit
    if isinstance(limit, bool) or not isinstance(limit, int):
        raise InvalidInputError("A limit must be a whole number.")
    return limit if limit > 0 else -1


def resolve_orders(
    entity: type[SQLModel], orders: Sequence[Order] | None
) -> tuple[Order, ...]:
    """Omitted Orders resolve to the configured default order; supplied Orders replace it and keep their sequence."""
    if orders:
        return tuple(orders)
    query = configuration.settings.query
    field_reference = getattr(entity, query.default_order_field, None)
    if not isinstance(field_reference, QueryableAttribute):
        raise InvalidInputError(
            "The default order names a Field this Entity does not have."
        )
    return (Order(field_reference, query.default_order_direction),)


def resolve_storage_location(instance: InstanceSpec) -> Path:
    """The storage file of a file-backed Instance, always beneath the Database-owned storage root."""
    root = (COMPONENT_ROOT / configuration.settings.storage_root).resolve()
    if (
        not root.is_relative_to(COMPONENT_ROOT.resolve())
        or root == COMPONENT_ROOT.resolve()
    ):
        raise ConfigurationError(
            "The storage root must be a directory inside the Database."
        )
    location = (root / instance.database).resolve()
    if not location.is_relative_to(root) or location == root:
        raise ConfigurationError(
            f"Instance '{instance.key}' names a storage location outside the Database storage."
        )
    return location
