"""The shared routing of every public request."""

import datetime
import decimal
import importlib
import json
import uuid
from collections.abc import Mapping
from types import ModuleType
from typing import Any

from pydantic import ValidationError

from database.core import query
from database.core.configuration import ResolvedInstance, configuration
from database.core.errors import (
    ConfigurationError,
    DeclarationMismatchError,
    ExecutionError,
    InactiveInstanceError,
    InvalidInputError,
)
from database.core.values import CommandResult, database_instance

_ZERO: dict[str, Any] = {"integer": 0, "float": 0.0, "decimal": decimal.Decimal(0)}


def resolve(instance: Any) -> tuple[database_instance, ResolvedInstance, ModuleType]:
    """The selected or default Instance, its configuration, and its Engine unit."""
    settings = configuration()
    if instance is None:
        instance = database_instance(settings.default_instance)
    if not isinstance(instance, database_instance):
        raise ConfigurationError("instance must be a DatabaseInstance member")
    resolved = settings.instances.get(instance.value)
    if resolved is None:
        raise ConfigurationError(f"Instance {instance.name} is not configured")
    if not resolved.active:
        raise InactiveInstanceError(f"Instance {instance.name} is inactive")
    name = f"database.engine.{resolved.engine}"
    try:
        unit = importlib.import_module(name)
    except ModuleNotFoundError as error:
        reason = (
            "has no Engine unit" if error.name == name else "cannot load its driver"
        )
        raise ConfigurationError(f"Instance {instance.name} engine {reason}") from None
    return instance, resolved, unit


def _json_value(value: Any) -> Any:
    if isinstance(value, decimal.Decimal | uuid.UUID):
        return str(value)
    if isinstance(value, datetime.date | datetime.time):
        return value.isoformat()
    return value


def materialize(entity: Any, row: Mapping[str, Any] | None) -> Any:
    """Build the Entity from a stored row through the Entity's own construction."""
    if row is None:
        return None
    names = [declared.name for declared in entity.declaration.fields]
    if set(row) != set(names):
        raise DeclarationMismatchError(
            f"a stored {entity.__name__} row does not hold exactly its Fields"
        )
    try:
        text = json.dumps(
            {name: _json_value(row[name]) for name in names}, allow_nan=False
        )
        return entity.from_json(text)
    except ValidationError as error:
        fields = sorted({".".join(map(str, item["loc"])) for item in error.errors()})
        raise DeclarationMismatchError(
            f"a stored {entity.__name__} row breaks the Entity contract"
            f" in {', '.join(fields) or 'its JSON Object'}"
        ) from None
    except TypeError, ValueError:
        raise DeclarationMismatchError(
            f"a stored {entity.__name__} row holds a value outside its Field Types"
        ) from None


def _auto_increment(declared: Any) -> bool:
    generation = declared.value_generation
    return generation is not None and generation.value == "auto_increment"


def _check_id(identifier: Any) -> int:
    if not isinstance(identifier, int) or isinstance(identifier, bool):
        raise InvalidInputError("id must be an integer")
    return identifier


def add(entity: Any, instance: Any = None) -> Any:
    kind = query.check_instance_of(entity)
    values: dict[str, Any] = {}
    for declared in kind.declaration.fields:
        value = getattr(entity, declared.name)
        if _auto_increment(declared):
            if value is not None:
                raise InvalidInputError(
                    f"add accepts a new Entity whose {declared.name} is pending"
                )
            continue
        values[declared.name] = value
    _, resolved, unit = resolve(instance)
    return materialize(kind, unit.insert(resolved, kind, values))


def update(entity: Any, instance: Any = None) -> Any:
    kind = query.check_instance_of(entity)
    identifier = entity.id
    values = {
        declared.name: getattr(entity, declared.name)
        for declared in kind.declaration.fields
        if not declared.immutable
    }
    _, resolved, unit = resolve(instance)
    if identifier is None:
        return None
    return materialize(kind, unit.update(resolved, kind, identifier, values))


def list_entities(
    entity: Any,
    filters: Any = None,
    combination: Any = None,
    orders: Any = None,
    limit: Any = None,
    instance: Any = None,
) -> list[Any]:
    kind = query.check_entity(entity)
    defaults = configuration().query
    checked, combined = query.check_filters(kind, filters, combination, defaults)
    ordering = query.check_orders(kind, orders, defaults)
    bound = query.check_limit(limit, defaults)
    _, resolved, unit = resolve(instance)
    rows = unit.select(resolved, kind, checked, combined, ordering, bound)
    return [materialize(kind, row) for row in rows]


def get_by_id(entity: Any, id: Any, instance: Any = None) -> Any:
    kind = query.check_entity(entity)
    identifier = _check_id(id)
    _, resolved, unit = resolve(instance)
    return materialize(kind, unit.get(resolved, kind, identifier))


def delete(entity: Any, id: Any, instance: Any = None) -> Any:
    kind = query.check_entity(entity)
    identifier = _check_id(id)
    _, resolved, unit = resolve(instance)
    return materialize(kind, unit.delete(resolved, kind, identifier))


def set_activity(entity: Any, id: Any, active: bool, instance: Any = None) -> Any:
    kind = query.check_entity(entity)
    identifier = _check_id(id)
    _, resolved, unit = resolve(instance)
    return materialize(kind, unit.set_activity(resolved, kind, identifier, active))


def count(
    entity: Any, filters: Any = None, combination: Any = None, instance: Any = None
) -> int:
    kind = query.check_entity(entity)
    defaults = configuration().query
    checked, combined = query.check_filters(kind, filters, combination, defaults)
    _, resolved, unit = resolve(instance)
    return int(unit.count(resolved, kind, checked, combined))


def aggregate(
    function: str,
    entity: Any,
    field: Any,
    filters: Any = None,
    combination: Any = None,
    instance: Any = None,
) -> Any:
    kind = query.check_entity(entity)
    name, field_type = query.check_aggregate_field(kind, field, function == "sum")
    defaults = configuration().query
    checked, combined = query.check_filters(kind, filters, combination, defaults)
    _, resolved, unit = resolve(instance)
    value = unit.aggregate(
        resolved, kind, function, name, field_type, checked, combined
    )
    if value is None and function == "sum":
        return _ZERO[field_type]
    return value


def truncate(entity: Any, instance: Any = None) -> int:
    kind = query.check_entity(entity)
    _, resolved, unit = resolve(instance)
    return int(unit.truncate(resolved, kind))


def execute_command(
    command: Any, parameters: Any = None, instance: Any = None
) -> CommandResult:
    if not isinstance(command, str) or not command.strip():
        raise InvalidInputError("command must be non-empty text")
    if parameters is not None and not isinstance(parameters, Mapping | list | tuple):
        raise InvalidInputError("parameters must be a mapping or a sequence")
    member, resolved, unit = resolve(instance)
    try:
        rows, affected, columns = unit.execute(resolved, command, parameters)
    except ExecutionError as error:
        return CommandResult(
            rows=None,
            affected=None,
            columns=None,
            success=False,
            message=str(error),
            instance=member,
        )
    if rows is not None:
        message = f"returned {len(rows)} rows"
    elif affected is not None:
        message = f"affected {affected} rows"
    else:
        message = "command completed"
    return CommandResult(
        rows=rows,
        affected=affected,
        columns=columns,
        success=True,
        message=message,
        instance=member,
    )
