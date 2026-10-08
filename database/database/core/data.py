"""Data (Core): the shared routing of every public request."""

from enum import Enum
from types import ModuleType
from typing import Any

from model import entities
from sqlalchemy.orm.attributes import set_committed_value

from database.core import configuration, query
from database.core.errors import (
    ConfigurationError,
    DeclarationMismatchError,
    InvalidInputError,
)
from database.core.values import (
    CheckedOrder,
    CommandResult,
    Connection,
    FilterCombination,
    OrderDirection,
)
from database.engine import sqlite

_ENGINES: dict[str, ModuleType] = {"sqlite": sqlite}


def entity_class(entity: Any) -> Any:
    """Return the Entity of the Model Entity Collection a class or instance is."""
    candidate = entity if isinstance(entity, type) else type(entity)
    if candidate not in entities:
        raise InvalidInputError("The Entity must come from the Model Entity Collection")
    return candidate


def _class_of(entity: Any) -> Any:
    if not isinstance(entity, type):
        raise InvalidInputError("An Entity class is required")
    return entity_class(entity)


def _instance_of(entity: Any) -> Any:
    if isinstance(entity, type):
        raise InvalidInputError("An Entity instance is required")
    return entity_class(entity)


def target(instance: Any) -> tuple[ModuleType, Connection, Enum]:
    selected = configuration.select_instance(instance)
    engine = _ENGINES.get(selected.engine)
    if engine is None:
        raise ConfigurationError(f"No Engine unit exists for {selected.engine!r}")
    member = configuration.instance_enum()(selected.key)
    return engine, configuration.connection(selected), member


def _materialize(cls: Any, row: dict[str, Any]) -> Any:
    """Build the Entity of a stored row through the Entity's own construction."""
    generated = {
        item.name
        for item in cls.declaration.fields
        if item.value_generation == "auto_increment"
    }
    values = {name: value for name, value in row.items() if name not in generated}
    try:
        entity = cls(**values)
    except ValueError, TypeError:
        raise DeclarationMismatchError(
            f"A stored row of {cls.__name__} does not satisfy its Entity contract"
        ) from None
    for name in generated:
        set_committed_value(entity, name, row[name])
    return entity


def _optional(cls: Any, row: dict[str, Any] | None) -> Any:
    return None if row is None else _materialize(cls, row)


def _combination(value: Any) -> FilterCombination:
    if value is None:
        return configuration.load().query.filter_combination
    if not isinstance(value, FilterCombination):
        raise InvalidInputError("The combination must be a FilterCombination member")
    return value


def _orders(cls: Any, orders: Any) -> tuple[CheckedOrder, ...]:
    checked = query.check_orders(cls, orders)
    if checked:
        return checked
    defaults = configuration.load().query
    declared = {item.name: item.type.value for item in cls.declaration.fields}
    if defaults.order_field not in declared:
        raise ConfigurationError(
            f"The default order Field {defaults.order_field!r} is not a Field of {cls.__name__}"
        )
    descending = defaults.order_direction is OrderDirection.DESCENDING
    return (
        CheckedOrder(defaults.order_field, declared[defaults.order_field], descending),
    )


def _limit(value: Any) -> int:
    if value is None:
        return configuration.load().query.default_limit
    if isinstance(value, bool) or not isinstance(value, int):
        raise InvalidInputError("The limit must be an integer")
    return value if value > 0 else -1


def add(entity: Any, instance: Any) -> Any:
    cls = _instance_of(entity)
    if entity.id is not None:
        raise InvalidInputError("Only a new Entity without an id can be added")
    values = {
        item.name: getattr(entity, item.name)
        for item in cls.declaration.fields
        if item.value_generation != "auto_increment"
    }
    engine, connection, _ = target(instance)
    return _materialize(cls, engine.add(connection, cls, values))


def update(entity: Any, instance: Any) -> Any:
    cls = _instance_of(entity)
    identity = query.check_identity(cls, entity.id)
    values = {
        item.name: getattr(entity, item.name)
        for item in cls.declaration.fields
        if not item.immutable
    }
    engine, connection, _ = target(instance)
    return _optional(cls, engine.replace(connection, cls, identity, values))


def list_all(
    entity: Any,
    filters: Any,
    combination: Any,
    orders: Any,
    limit: Any,
    instance: Any,
) -> list[Any]:
    cls = _class_of(entity)
    checked_filters = query.check_filters(cls, filters)
    resolved_combination = _combination(combination)
    checked_orders = _orders(cls, orders)
    resolved_limit = _limit(limit)
    engine, connection, _ = target(instance)
    rows = engine.list_rows(
        connection,
        cls,
        checked_filters,
        resolved_combination,
        checked_orders,
        resolved_limit,
    )
    return [_materialize(cls, row) for row in rows]


def get_by_id(entity: Any, id: Any, instance: Any) -> Any:
    cls = _class_of(entity)
    identity = query.check_identity(cls, id)
    engine, connection, _ = target(instance)
    return _optional(cls, engine.get_by_id(connection, cls, identity))


def delete(entity: Any, id: Any, instance: Any) -> Any:
    cls = _class_of(entity)
    identity = query.check_identity(cls, id)
    engine, connection, _ = target(instance)
    return _optional(cls, engine.remove(connection, cls, identity))


def set_active(entity: Any, id: Any, active: bool, instance: Any) -> Any:
    cls = _class_of(entity)
    identity = query.check_identity(cls, id)
    engine, connection, _ = target(instance)
    return _optional(cls, engine.set_active(connection, cls, identity, active))


def count(entity: Any, filters: Any, combination: Any, instance: Any) -> int:
    cls = _class_of(entity)
    checked_filters = query.check_filters(cls, filters)
    resolved_combination = _combination(combination)
    engine, connection, _ = target(instance)
    return engine.count(connection, cls, checked_filters, resolved_combination)


def total(
    entity: Any, field: Any, filters: Any, combination: Any, instance: Any
) -> Any:
    cls = _class_of(entity)
    checked_field = query.numeric_field_of(cls, field)
    checked_filters = query.check_filters(cls, filters)
    resolved_combination = _combination(combination)
    engine, connection, _ = target(instance)
    return engine.total(
        connection, cls, checked_field, checked_filters, resolved_combination
    )


def extreme(
    entity: Any,
    field: Any,
    filters: Any,
    combination: Any,
    largest: bool,
    instance: Any,
) -> Any:
    cls = _class_of(entity)
    checked_field = query.field_of(cls, field)
    checked_filters = query.check_filters(cls, filters)
    resolved_combination = _combination(combination)
    engine, connection, _ = target(instance)
    return engine.extreme(
        connection, cls, checked_field, checked_filters, resolved_combination, largest
    )


def truncate(entity: Any, instance: Any) -> int:
    cls = _class_of(entity)
    engine, connection, _ = target(instance)
    return engine.truncate(connection, cls)


def execute_command(command: Any, parameters: Any, instance: Any) -> CommandResult:
    if not isinstance(command, str) or not command.strip():
        raise InvalidInputError("The command must be a non-empty string")
    if parameters is not None and not isinstance(parameters, dict | list | tuple):
        raise InvalidInputError("The parameters must be a mapping or a sequence")
    engine, connection, member = target(instance)
    bound = tuple(parameters) if isinstance(parameters, list) else parameters
    rows, affected, columns = engine.execute_command(connection, command, bound)
    return CommandResult(
        rows=rows,
        affected=affected,
        columns=columns,
        success=True,
        message="Command executed",
        instance=member,
    )
