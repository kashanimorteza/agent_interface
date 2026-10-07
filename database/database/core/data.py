import builtins
import importlib
from collections.abc import Mapping, Sequence
from functools import cache
from types import MappingProxyType, ModuleType
from typing import Any

from sqlalchemy.orm.attributes import set_committed_value

from database.core.configuration import (
    CONFIGURATION,
    Connection,
    member_name,
    resolve_connection,
    resolve_instance,
)
from database.core.errors import ConfigurationError, ExecutionError, InvalidInputError
from database.core.query import (
    check_filters,
    resolve_combination,
    resolve_limit,
    resolve_orders,
)
from database.core.tables import (
    check_aggregate_field,
    check_entity_class,
    check_entity_instance,
    check_id,
)
from database.core.values import (
    CommandResult,
    DatabaseInstance,
    Filter,
    FilterCombination,
    Order,
)


@cache
def _unit(engine: str) -> ModuleType:
    try:
        return importlib.import_module(f"database.engine.{engine}")
    except ImportError:
        raise ConfigurationError(f"There is no Engine unit for the Engine {engine}.") from None


def resolve(selection: DatabaseInstance | None) -> tuple[ModuleType, Connection]:
    """Resolve the selected Instance to the Engine unit of its Engine and its connection."""
    connection = resolve_connection(resolve_instance(selection))
    return _unit(connection.engine), connection


def route(selection: DatabaseInstance | None, operation: str, *arguments: Any) -> Any:
    """Forward a validated request with the Instance's connection to its Engine unit."""
    unit, connection = resolve(selection)
    capability = getattr(unit, operation, None)
    if capability is None:
        raise ConfigurationError(f"The Engine unit of {connection.engine} lacks {operation}.")
    return capability(connection, *arguments)


def materialize(entity: type[Any], row: Mapping[str, Any]) -> Any:
    """Build an Entity from a stored row through the Entity's own construction.

    A Field whose value storage generates is not accepted by construction, so the Entity is built
    from every other Field and the stored value of the generated Field is then attached.
    """
    name = entity.declaration.name
    fields = entity.declaration.fields
    try:
        values = {f.name: row[f.name] for f in fields if f.value_generation is None}
        instance = entity(**values)
    except (KeyError, ValueError) as error:
        listed = getattr(error, "errors", None)
        names = sorted({str(item["loc"][0]) for item in listed()}) if listed else []
        detail = f" (Fields: {', '.join(names)})" if names else ""
        raise ExecutionError(
            f"A stored row of {name} does not satisfy the Entity contract{detail}."
        ) from None
    for field in fields:
        if field.value_generation is not None:
            set_committed_value(instance, field.name, row[field.name])
    return instance


def _identity(entity: type[Any]) -> str:
    return entity.declaration.primary_key


def _row_to_entity(entity: type[Any], row: Mapping[str, Any] | None) -> Any:
    """A missing record is nothing, never an error."""
    return None if row is None else materialize(entity, row)


def add(entity: Any, instance: DatabaseInstance | None) -> Any:
    entity_class = check_entity_instance(entity)
    if getattr(entity, _identity(entity_class)) is not None:
        raise InvalidInputError("Only a new Entity, whose identity is still pending, can be added.")
    values = {
        field.name: getattr(entity, field.name)
        for field in entity_class.declaration.fields
        if field.value_generation is None
    }
    return materialize(entity_class, route(instance, "add", entity_class, values))


def update(entity: Any, instance: DatabaseInstance | None) -> Any:
    entity_class = check_entity_instance(entity)
    identity = getattr(entity, _identity(entity_class))
    if identity is None:
        raise InvalidInputError("Only a stored Entity, which has an id, can be updated.")
    values = {
        field.name: getattr(entity, field.name)
        for field in entity_class.declaration.fields
        if not field.immutable
    }
    row = route(instance, "update", entity_class, identity, values)
    return _row_to_entity(entity_class, row)


def list_entities(
    entity: Any,
    filters: Sequence[Filter] | None,
    combination: FilterCombination | None,
    orders: Sequence[Order] | None,
    limit: int | None,
    instance: DatabaseInstance | None,
) -> builtins.list[Any]:
    entity_class = check_entity_class(entity)
    checked = check_filters(entity_class, filters)
    chosen = resolve_combination(combination, CONFIGURATION.query.combination)
    ordering = resolve_orders(entity_class, orders, CONFIGURATION.query)
    cap = resolve_limit(limit, CONFIGURATION.query)
    rows = route(instance, "list_rows", entity_class, checked, chosen, ordering, cap)
    return [materialize(entity_class, row) for row in rows]


def get_by_id(entity: Any, identity: Any, instance: DatabaseInstance | None) -> Any:
    entity_class = check_entity_class(entity)
    identity = check_id(entity_class, identity)
    return _row_to_entity(entity_class, route(instance, "get_by_id", entity_class, identity))


def delete(entity: Any, identity: Any, instance: DatabaseInstance | None) -> Any:
    entity_class = check_entity_class(entity)
    identity = check_id(entity_class, identity)
    return _row_to_entity(entity_class, route(instance, "delete", entity_class, identity))


def set_active(entity: Any, identity: Any, active: bool, instance: DatabaseInstance | None) -> Any:
    entity_class = check_entity_class(entity)
    identity = check_id(entity_class, identity)
    row = route(instance, "set_active", entity_class, identity, active)
    return _row_to_entity(entity_class, row)


def count(
    entity: Any,
    filters: Sequence[Filter] | None,
    combination: FilterCombination | None,
    instance: DatabaseInstance | None,
) -> int:
    entity_class = check_entity_class(entity)
    checked = check_filters(entity_class, filters)
    chosen = resolve_combination(combination, CONFIGURATION.query.combination)
    return route(instance, "count", entity_class, checked, chosen)


def aggregate(
    operation: str,
    entity: Any,
    field: Any,
    filters: Sequence[Filter] | None,
    combination: FilterCombination | None,
    instance: DatabaseInstance | None,
) -> Any:
    """Sum, smallest, or largest value of one Field; operation names the Engine capability."""
    entity_class = check_entity_class(entity)
    declaration = check_aggregate_field(entity_class, field, numeric=operation == "sum_values")
    checked = check_filters(entity_class, filters)
    chosen = resolve_combination(combination, CONFIGURATION.query.combination)
    return route(instance, operation, entity_class, declaration, checked, chosen)


def truncate(entity: Any, instance: DatabaseInstance | None) -> int:
    entity_class = check_entity_class(entity)
    return route(instance, "truncate", entity_class)


def execute_command(
    command: Any, parameters: Mapping[str, Any] | None, instance: DatabaseInstance | None
) -> CommandResult:
    if not isinstance(command, str) or not command.strip():
        raise InvalidInputError("The command must be a non-empty native command text.")
    if parameters is None:
        parameters = {}
    if not isinstance(parameters, Mapping) or not all(isinstance(key, str) for key in parameters):
        raise InvalidInputError("The command parameters must be a mapping of names to values.")
    selected = resolve_instance(instance)
    outcome = route(instance, "execute", command, parameters)
    rows = outcome["rows"]
    columns = outcome["columns"]
    return CommandResult(
        rows=None if rows is None else tuple(MappingProxyType(row) for row in rows),
        affected=outcome["affected"],
        columns=None if columns is None else tuple(columns),
        success=True,
        message="The command was executed.",
        instance=DatabaseInstance[member_name(selected.key)],
    )
