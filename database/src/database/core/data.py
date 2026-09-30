"""Shared validation, defaults, Instance selection, routing, and result normalization.

Every public request passes through here. It validates input before any Instance is
touched, resolves defaults and the selected Instance, forwards the request to that
Instance's implementation, and returns the result in its published form. It holds no
driver call and no Instance-specific storage behaviour.
"""

import builtins
import importlib
from collections.abc import Collection, Mapping, Sequence
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, cast

from sqlmodel import SQLModel

from database.core._config import Configuration, load_configuration
from database.core._contracts import (
    NULL_TESTING,
    TEXTUAL,
    CommandResult,
    DatabaseInstance,
    Filter,
    FilterCombination,
    FilterOperator,
    Order,
    OrderDirection,
    Query,
)
from database.core._engine import Engine, Record
from database.core._entities import declarations, entity_classes, identity_of
from database.core._failures import (
    ConfigurationFailure,
    InstanceInactiveFailure,
    InvalidInputFailure,
    sanitized,
)

_state: dict[str, Any] = {
    "path": None,
    "configuration": None,
    "engines": {},
}


def use_configuration(path: Path | None) -> None:
    """Select the configuration file to load (default: the Component's) and reset."""
    _state.update(path=path, configuration=None, engines={})


def configuration() -> Configuration:
    if _state["configuration"] is None:
        _state["configuration"] = load_configuration(_state["path"])
    return cast(Configuration, _state["configuration"])


# ---------------------------------------------------------------- Instance selection
def select_instance(instance: DatabaseInstance | None) -> str:
    """Resolve the Instance key for a request; reject an unusable selection."""
    loaded = configuration()
    if instance is None:
        return loaded.default_instance
    if not isinstance(instance, DatabaseInstance):  # pyright: ignore[reportUnnecessaryIsInstance]
        raise ConfigurationFailure(
            "An Instance is selected through a DatabaseInstance member."
        )
    if instance.value not in loaded.instances:
        raise ConfigurationFailure(
            "The selected Instance is not declared in the configuration."
        )
    if not loaded.instances[instance.value].active:
        raise InstanceInactiveFailure("The selected Instance is not active.")
    return instance.value


def engine_for(key: str) -> Engine:
    """The one implementation of an Instance, created on first use."""
    engines = cast(dict[str, Engine], _state["engines"])
    if key not in engines:
        loaded = configuration()
        definition = loaded.instances[key]
        module = importlib.import_module(f"database.engine.{key}")
        engines[key] = module.create(
            loaded, loaded.engines[definition.engine], definition, declarations()
        )
    return engines[key]


# --------------------------------------------------------------------------- validation
def _identity_of_class(entity: Any) -> str:
    if isinstance(entity, str):
        raise InvalidInputFailure(
            "An Entity is selected by its class, never by a name."
        )
    identity = identity_of(entity) if isinstance(entity, type) else None
    if identity is None:
        raise InvalidInputFailure("The request must name a public Entity class.")
    return identity


def _identity_of_instance(entity: Any) -> str:
    identity = identity_of(cast(type[SQLModel], type(entity)))
    if identity is None:
        raise InvalidInputFailure("The request must carry a public Entity instance.")
    return identity


def _field(identity: str, name: Any) -> Any:
    if isinstance(name, str):
        for declared in declarations()[identity].fields:
            if declared.name == name:
                return declared
    raise InvalidInputFailure(f"{declarations()[identity].name} has no such Field.")


_INT64 = (-(2**63), 2**63 - 1)


def _compatible(declared: Any, value: Any) -> bool:
    kind: str = declared.type
    if kind == "integer":
        return type(value) is int and _INT64[0] <= value <= _INT64[1]
    if kind == "float":
        return type(value) in (int, float)
    if kind == "decimal":
        return type(value) in (int, Decimal) and (
            type(value) is int or value.is_finite()
        )
    if kind == "string":
        return isinstance(value, str) and "\x00" not in value
    if kind == "boolean":
        return type(value) is bool
    if kind == "datetime":
        return isinstance(value, datetime) and value.tzinfo is not None
    return False


def _validate_filter(identity: str, item: Any) -> Filter:
    if not isinstance(item, Filter):
        raise InvalidInputFailure("Filters are Filter values.")
    declared = _field(identity, item.field)
    operator = item.operator
    if operator in NULL_TESTING:
        return item
    if operator in TEXTUAL and declared.type != "string":
        raise InvalidInputFailure(f"{operator.name} needs a textual Field.")
    values: Collection[Any] = (
        item.value if operator is FilterOperator.IN else (item.value,)
    )
    for value in values:
        if operator in TEXTUAL and not isinstance(value, str):
            raise InvalidInputFailure(f"{operator.name} needs a textual value.")
        if not _compatible(declared, value):
            raise InvalidInputFailure(
                "A Filter value is not compatible with its Field."
            )
    return item


def _query(
    identity: str,
    filters: Sequence[Filter] | None,
    combination: FilterCombination | None,
    orders: Sequence[Order] | None,
    limit: int | None,
    *,
    ordered: bool,
) -> Query:
    defaults = configuration().query
    if filters is None:
        checked: tuple[Filter, ...] = ()
    elif isinstance(filters, (str, bytes, Mapping)) or not isinstance(
        filters, Sequence
    ):  # pyright: ignore[reportUnnecessaryIsInstance]
        raise InvalidInputFailure("Filters are a sequence of Filter values.")
    else:
        checked = tuple(_validate_filter(identity, item) for item in filters)
    if combination is None:
        combination = defaults.filter_combination
    elif not isinstance(combination, FilterCombination):  # pyright: ignore[reportUnnecessaryIsInstance]
        raise InvalidInputFailure("A combination is a FilterCombination member.")
    if not ordered:
        if orders is not None or limit is not None:
            raise InvalidInputFailure("Only List accepts Orders and a limit.")
        return Query(checked, combination, (), -1)
    if orders is None or len(orders) == 0:
        chosen: tuple[Order, ...] = (
            Order(defaults.order_field, defaults.order_direction),
        )
    elif isinstance(orders, (str, bytes, Mapping)) or not isinstance(orders, Sequence):  # pyright: ignore[reportUnnecessaryIsInstance]
        raise InvalidInputFailure("Orders are a sequence of Order values.")
    else:
        chosen = tuple(orders)
    for order in chosen:
        if not isinstance(order, Order):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise InvalidInputFailure("Orders are Order values.")
        _field(identity, order.field)
    if limit is None:
        limit = defaults.default_limit
    elif not isinstance(limit, int) or isinstance(limit, bool):  # pyright: ignore[reportUnnecessaryIsInstance]
        raise InvalidInputFailure("A limit is an integer.")
    return Query(checked, combination, chosen, limit if limit > 0 else -1)


def _identifier(value: Any) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise InvalidInputFailure("An identifier is an integer.")
    if not _INT64[0] <= value <= _INT64[1]:
        raise InvalidInputFailure("An identifier is a 64-bit integer.")
    return value


def _storable(declared: Any, value: Any) -> Any:
    """A Field value every Instance can store, or a refusal that names no value."""
    if value is not None and declared.type in ("integer", "string"):
        if not _compatible(declared, value):
            raise InvalidInputFailure(
                f"A {declared.type} Field holds a value no Instance can store."
            )
    return value


# ------------------------------------------------------------ result materialization
def _encode(declared: Any, value: Any) -> Any:
    if value is None:
        return None
    if declared.type == "decimal":
        return format(Decimal(value).normalize(), "f")
    if declared.type == "datetime":
        return value.isoformat()
    return value


def materialize(identity: str, record: Record) -> Any:
    """Return a stored record as its public Entity instance."""
    declaration = declarations()[identity]
    entity = cast(Any, entity_classes()[identity])
    return entity.from_json(
        {
            declared.name: _encode(declared, record[declared.name])
            for declared in declaration.fields
        }
    )


def _mutable_values(identity: str, entity: Any) -> dict[str, Any]:
    return {
        declared.name: _storable(declared, getattr(entity, declared.name))
        for declared in declarations()[identity].fields
        if not declared.immutable and declared.value_generation is None
    }


def stored_values(identity: str, entity: Any) -> dict[str, Any]:
    """Every supplied (not generated) Field value of an Entity instance."""
    return {
        declared.name: _storable(declared, getattr(entity, declared.name))
        for declared in declarations()[identity].fields
        if declared.value_generation is None
    }


# ------------------------------------------------------------------- Entity Operations
@sanitized
def add[E: SQLModel](entity: E, instance: DatabaseInstance | None) -> E:
    identity = _identity_of_instance(entity)
    if getattr(entity, "id") is not None:  # noqa: B009
        raise InvalidInputFailure("A new Entity has no identifier.")
    engine = engine_for(select_instance(instance))
    return cast(
        E, materialize(identity, engine.add(identity, stored_values(identity, entity)))
    )


@sanitized
def update[E: SQLModel](entity: E, instance: DatabaseInstance | None) -> E | None:
    identity = _identity_of_instance(entity)
    identifier = getattr(entity, "id")  # noqa: B009
    if identifier is None:
        raise InvalidInputFailure("An Entity to update carries its identifier.")
    engine = engine_for(select_instance(instance))
    record = engine.update(
        identity, _identifier(identifier), _mutable_values(identity, entity)
    )
    return None if record is None else cast(E, materialize(identity, record))


@sanitized
def get_by_id[E: SQLModel](
    entity: type[E], identifier: int, instance: DatabaseInstance | None
) -> E | None:
    identity = _identity_of_class(entity)
    number = _identifier(identifier)
    record = engine_for(select_instance(instance)).get_by_id(identity, number)
    return None if record is None else cast(E, materialize(identity, record))


@sanitized
def delete[E: SQLModel](
    entity: type[E], identifier: int, instance: DatabaseInstance | None
) -> E | None:
    identity = _identity_of_class(entity)
    number = _identifier(identifier)
    record = engine_for(select_instance(instance)).delete(identity, number)
    return None if record is None else cast(E, materialize(identity, record))


@sanitized
def enable[E: SQLModel](
    entity: type[E], identifier: int, instance: DatabaseInstance | None
) -> E | None:
    identity = _identity_of_class(entity)
    number = _identifier(identifier)
    record = engine_for(select_instance(instance)).enable(identity, number)
    return None if record is None else cast(E, materialize(identity, record))


@sanitized
def disable[E: SQLModel](
    entity: type[E], identifier: int, instance: DatabaseInstance | None
) -> E | None:
    identity = _identity_of_class(entity)
    number = _identifier(identifier)
    record = engine_for(select_instance(instance)).disable(identity, number)
    return None if record is None else cast(E, materialize(identity, record))


@sanitized
def list_[E: SQLModel](
    entity: type[E],
    filters: Sequence[Filter] | None,
    combination: FilterCombination | None,
    orders: Sequence[Order] | None,
    limit: int | None,
    instance: DatabaseInstance | None,
) -> builtins.list[E]:
    identity = _identity_of_class(entity)
    query = _query(identity, filters, combination, orders, limit, ordered=True)
    records = engine_for(select_instance(instance)).list(identity, query)
    return [cast(E, materialize(identity, record)) for record in records]


@sanitized
def count(
    entity: type[SQLModel],
    filters: Sequence[Filter] | None,
    combination: FilterCombination | None,
    instance: DatabaseInstance | None,
) -> int:
    identity = _identity_of_class(entity)
    query = _query(identity, filters, combination, None, None, ordered=False)
    return int(engine_for(select_instance(instance)).count(identity, query))


_NUMERIC = ("integer", "float", "decimal")
_COMPARABLE = (*_NUMERIC, "string", "datetime")


def _aggregate_field(identity: str, field: str, allowed: tuple[str, ...]) -> Any:
    declared = _field(identity, field)
    if declared.type not in allowed:
        raise InvalidInputFailure("The Field's type does not support this aggregate.")
    return declared


def _aggregate(
    function: str,
    entity: type[SQLModel],
    field: str,
    filters: Sequence[Filter] | None,
    combination: FilterCombination | None,
    instance: DatabaseInstance | None,
) -> Any:
    identity = _identity_of_class(entity)
    declared = _aggregate_field(
        identity, field, _NUMERIC if function == "sum" else _COMPARABLE
    )
    query = _query(identity, filters, combination, None, None, ordered=False)
    engine = engine_for(select_instance(instance))
    value = getattr(engine, function)(identity, field, query)
    if value is None:
        return (
            {"integer": 0, "float": 0.0, "decimal": Decimal(0)}[declared.type]
            if function == "sum"
            else None
        )
    if declared.type == "decimal":
        return Decimal(value)
    if declared.type == "float":
        return float(value)
    if declared.type == "integer" and function == "sum":
        return int(value)
    return value


@sanitized
def sum_(
    entity: type[SQLModel],
    field: str,
    filters: Sequence[Filter] | None,
    combination: FilterCombination | None,
    instance: DatabaseInstance | None,
) -> Any:
    return _aggregate("sum", entity, field, filters, combination, instance)


@sanitized
def min_(
    entity: type[SQLModel],
    field: str,
    filters: Sequence[Filter] | None,
    combination: FilterCombination | None,
    instance: DatabaseInstance | None,
) -> Any:
    return _aggregate("min", entity, field, filters, combination, instance)


@sanitized
def max_(
    entity: type[SQLModel],
    field: str,
    filters: Sequence[Filter] | None,
    combination: FilterCombination | None,
    instance: DatabaseInstance | None,
) -> Any:
    return _aggregate("max", entity, field, filters, combination, instance)


@sanitized
def truncate(entity: type[SQLModel], instance: DatabaseInstance | None) -> int:
    identity = _identity_of_class(entity)
    return int(engine_for(select_instance(instance)).truncate(identity))


# ------------------------------------------------------------ Database-wide Operation
@sanitized
def execute_command(
    command: str,
    parameters: Mapping[str, Any] | None,
    instance: DatabaseInstance | None,
) -> CommandResult:
    if not isinstance(command, str) or not command.strip():  # pyright: ignore[reportUnnecessaryIsInstance]
        raise InvalidInputFailure("A command is non-empty SQL text.")
    if parameters is not None and not isinstance(parameters, Mapping):  # pyright: ignore[reportUnnecessaryIsInstance]
        raise InvalidInputFailure("Parameters are a mapping of names to values.")
    key = select_instance(instance)
    rows, affected, columns = engine_for(key).execute_command(
        command, dict(parameters or {})
    )
    return CommandResult(
        rows,
        affected,
        columns,
        True,
        "The command was executed.",
        DatabaseInstance(key),
    )


__all__ = [
    "OrderDirection",
    "add",
    "configuration",
    "count",
    "delete",
    "disable",
    "enable",
    "engine_for",
    "execute_command",
    "get_by_id",
    "list_",
    "materialize",
    "max_",
    "min_",
    "select_instance",
    "stored_values",
    "sum_",
    "truncate",
    "update",
    "use_configuration",
]
