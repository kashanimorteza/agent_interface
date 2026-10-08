"""Data: the shared routing of every public request."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

import model
from sqlalchemy.orm.attributes import set_attribute

from . import configuration as configuring
from .configuration import Configuration, Connection
from .errors import (
    ConfigurationError,
    ExecutionError,
    InactiveInstanceError,
    InvalidInputError,
)
from .query import (
    check_aggregate,
    check_filters,
    compatible,
    resolve_combination,
    resolve_limit,
    resolve_orders,
)
from .values import CommandResult, database_instance

_loaded: Configuration | None = None


def configuration() -> Configuration:
    """Return the Database Configuration, loading and validating it on first use."""
    global _loaded
    if _loaded is None:
        _loaded = configuring.load()
    return _loaded


@dataclass(frozen=True, slots=True)
class Selected:
    """The Instance a request runs on, with its Engine unit and resolved connection."""

    member: database_instance
    unit: Any
    connection: Connection


def entity_class(entity: Any) -> Any:
    """Return an Entity class imported from Model, or refuse anything else (such as an Entity name)."""
    if not isinstance(entity, type) or entity not in model.entities:
        raise InvalidInputError("An entity must be an Entity class imported from Model")
    return entity


def entity_instance(entity: Any) -> Any:
    """Return an Entity instance of Model, or refuse anything else."""
    if type(entity) not in model.entities:
        raise InvalidInputError("An entity must be an Entity instance of Model")
    return entity


def identifier(entity: Any, value: Any) -> Any:
    """Return an identifier that suits the Entity's Primary Key Field, or refuse it."""
    declaration = entity.declaration
    for item in declaration.fields:
        if item.name == declaration.primary_key:
            if value is None or not compatible(str(item.type), value):
                raise InvalidInputError(
                    f"An id for {entity.__name__} must suit its {item.name} Field"
                )
            return value
    raise InvalidInputError(f"{entity.__name__} has no Primary Key Field")


def instance_member(instance: Any) -> database_instance | None:
    """Return the given Instance member, or None when none is given, refusing anything else."""
    if instance is None or isinstance(instance, database_instance):
        return instance
    raise InvalidInputError("An instance must be a database_instance member")


def resolve(loaded: Configuration, key: str) -> Selected:
    """Resolve one Instance by key before any storage is touched."""
    configured = loaded.instances.get(key)
    if configured is None:
        raise ConfigurationError(f"The Instance {key!r} is not configured")
    if not configured.active:
        raise InactiveInstanceError(f"The Instance {key!r} is not active")
    return Selected(
        member=database_instance(key),
        unit=configuring.engine_unit(configured.engine),
        connection=configuring.connection(loaded.settings, configured),
    )


def select(instance: Any) -> Selected:
    """Select the given Instance or, when none is given, the configured default Instance."""
    member = instance_member(instance)
    loaded = configuration()
    return resolve(loaded, member.value if member else loaded.settings.default_instance)


def forward(selected: Selected, operation: str, *arguments: Any) -> Any:
    """Hand a validated request and the Instance's connection to its Engine unit and return the raw result."""
    work = getattr(selected.unit, operation)
    with selected.unit.scope(selected.connection) as session:
        return work(session, *arguments)


def materialize(entity: Any, row: Mapping[str, Any] | None) -> Any:
    """Build the Entity of a stored row through its own construction, or return None when there is no row.

    The Entity is constructed from every Field value except the Auto Increment Field, which stays pending
    during construction as the Entity requires; the value storage assigned is then set on the built Entity.
    A row that does not satisfy the Entity's contract is an error and is never repaired.
    """
    if row is None:
        return None
    assigned = [
        item.name
        for item in entity.declaration.fields
        if str(item.value_generation) == "auto_increment"
    ]
    try:
        built = entity(
            **{name: value for name, value in row.items() if name not in assigned}
        )
    except ValueError, TypeError:
        raise ExecutionError(
            f"A stored row of {entity.__name__} does not satisfy its Entity"
        ) from None
    for name in assigned:
        set_attribute(built, name, row[name])
    return built


def command_result(
    selected: Selected,
    rows: list[dict[str, Any]] | None,
    affected: int | None,
    columns: list[str] | None,
) -> CommandResult:
    """Return the published Command Result of a native command that succeeded."""
    return CommandResult(
        rows=None if rows is None else tuple(rows),
        affected=affected,
        columns=None if columns is None else tuple(columns),
        success=True,
        message="The command succeeded",
        instance=selected.member,
    )


def _list_arguments(
    entity: Any, filters: Any, combination: Any, orders: Any, limit: Any, defaults: Any
) -> tuple[Any, ...]:
    return (
        check_filters(entity, filters),
        resolve_combination(defaults, combination),
        resolve_orders(entity, defaults, orders),
        resolve_limit(defaults, limit),
    )


def add(entity: Any, instance: Any) -> Any:
    """Store one complete new Entity and return the stored Entity, including generated values."""
    stored = entity_instance(entity)
    cls = type(stored)
    identity = cls.declaration.primary_key
    if getattr(stored, identity) is not None:
        raise InvalidInputError("The entity to add is already stored")
    selected = select(instance)
    values = {
        name: getattr(stored, name)
        for name in cls.model_fields
        if not (name == identity and getattr(stored, name) is None)
    }
    return materialize(cls, forward(selected, "add", cls, values))


def update(entity: Any, instance: Any) -> Any:
    """Replace every mutable Field of the stored record the Entity identifies and return it, or None when none exists."""
    stored = entity_instance(entity)
    cls = type(stored)
    identifier_value = identifier(cls, getattr(stored, cls.declaration.primary_key))
    selected = select(instance)
    values = {
        item.name: getattr(stored, item.name)
        for item in cls.declaration.fields
        if not item.immutable
    }
    return materialize(
        cls, forward(selected, "update_row", cls, identifier_value, values)
    )


def get_by_id(entity: Any, id: Any, instance: Any) -> Any:
    """Return the Entity stored under an identifier, or None when no such record exists."""
    cls = entity_class(entity)
    key = identifier(cls, id)
    return materialize(cls, forward(select(instance), "get_by_id", cls, key))


def delete(entity: Any, id: Any, instance: Any) -> Any:
    """Remove the record stored under an identifier and return the final deleted Entity, or None when none exists."""
    cls = entity_class(entity)
    key = identifier(cls, id)
    return materialize(cls, forward(select(instance), "delete_row", cls, key))


def enable(entity: Any, id: Any, instance: Any) -> Any:
    """Set only the activity Field to true and return the final Entity, or None when no record exists."""
    cls = entity_class(entity)
    key = identifier(cls, id)
    return materialize(cls, forward(select(instance), "set_active", cls, key, True))


def disable(entity: Any, id: Any, instance: Any) -> Any:
    """Set only the activity Field to false and return the final Entity, or None when no record exists."""
    cls = entity_class(entity)
    key = identifier(cls, id)
    return materialize(cls, forward(select(instance), "set_active", cls, key, False))


def list_entities(
    entity: Any,
    filters: Any,
    combination: Any,
    orders: Any,
    limit: Any,
    instance: Any,
) -> list[Any]:
    """Return the Entities that satisfy the Filters, ordered as given and bounded by the limit."""
    cls = entity_class(entity)
    selected = select(instance)
    arguments = _list_arguments(
        cls, filters, combination, orders, limit, configuration().settings.query
    )
    rows = forward(selected, "list_rows", cls, *arguments)
    return [materialize(cls, row) for row in rows]


def count(entity: Any, filters: Any, combination: Any, instance: Any) -> int:
    """Return the number of Entities that satisfy the Filters."""
    cls = entity_class(entity)
    checked = check_filters(cls, filters)
    selected = select(instance)
    mode = resolve_combination(configuration().settings.query, combination)
    return forward(selected, "count", cls, checked, mode)


def _aggregate(
    kind: str,
    operation: str,
    entity: Any,
    field: Any,
    filters: Any,
    combination: Any,
    instance: Any,
) -> Any:
    cls = entity_class(entity)
    name, type_name = check_aggregate(cls, field, kind)
    checked = check_filters(cls, filters)
    selected = select(instance)
    mode = resolve_combination(configuration().settings.query, combination)
    if kind == "sum":
        return forward(selected, operation, cls, name, type_name, checked, mode)
    return forward(selected, operation, cls, name, checked, mode)


def total(
    entity: Any, field: Any, filters: Any, combination: Any, instance: Any
) -> Any:
    """Return the total of a numeric Field over the matching Entities, or zero when nothing matches."""
    return _aggregate("sum", "total", entity, field, filters, combination, instance)


def smallest(
    entity: Any, field: Any, filters: Any, combination: Any, instance: Any
) -> Any:
    """Return the smallest value of a comparable Field over the matching Entities, or None when nothing matches."""
    return _aggregate("min", "smallest", entity, field, filters, combination, instance)


def largest(
    entity: Any, field: Any, filters: Any, combination: Any, instance: Any
) -> Any:
    """Return the largest value of a comparable Field over the matching Entities, or None when nothing matches."""
    return _aggregate("max", "largest", entity, field, filters, combination, instance)


def truncate(entity: Any, instance: Any) -> int:
    """Remove every record of an Entity, keeping its Table, and return how many were removed."""
    cls = entity_class(entity)
    return forward(select(instance), "truncate", cls)


def execute_command(command: Any, parameters: Any, instance: Any) -> CommandResult:
    """Run a native command with its bound parameters on the Instance and return the Command Result."""
    if not isinstance(command, str) or command.strip() == "":
        raise InvalidInputError("A command must be a non-empty string")
    if parameters is not None and not isinstance(parameters, (Mapping, list, tuple)):
        raise InvalidInputError("Command parameters must be a mapping or a sequence")
    selected = select(instance)
    rows, affected, columns = forward(selected, "execute_command", command, parameters)
    return command_result(selected, rows, affected, columns)
