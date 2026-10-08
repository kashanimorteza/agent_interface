"""Initial Data (Core): the insert-initial-data Setup Operation."""

from datetime import date, datetime, time
from decimal import Decimal
from typing import Any
from uuid import UUID

from model import entities

from database.core import configuration, data
from database.core.errors import InvalidInputError
from database.core.values import SetupResult


def _decoded(type_name: str, value: Any) -> Any:
    """Return a Configuration value in the Python form of the declared Type."""
    plain = isinstance(value, int | float | str) and not isinstance(value, bool)
    match type_name:
        case "decimal" if plain:
            return Decimal(str(value))
        case "float" if isinstance(value, int) and not isinstance(value, bool):
            return float(value)
        case "datetime" if isinstance(value, str):
            return datetime.fromisoformat(value)
        case "date" if isinstance(value, str):
            return date.fromisoformat(value)
        case "time" if isinstance(value, str):
            return time.fromisoformat(value)
        case "uuid" if isinstance(value, str):
            return UUID(value)
    return value


def _values(entity: Any, record: dict[str, Any]) -> dict[str, Any]:
    """Validate a record through the Entity's public contract; return its values."""
    types = {item.name: item.type.value for item in entity.declaration.fields}
    try:
        built = entity(
            **{
                name: _decoded(types.get(name, ""), item)
                for name, item in record.items()
            }
        )
    except ArithmeticError, ValueError, TypeError:
        raise InvalidInputError(
            f"An Initial Data record of {entity.__name__} breaks its Entity contract"
        ) from None
    return {
        item.name: getattr(built, item.name)
        for item in entity.declaration.fields
        if item.value_generation != "auto_increment"
    }


def insert_initial_data(instance: Any) -> SetupResult:
    """Insert the missing Initial Data records on the Instance, repeatably."""
    engine, connection, member = data.target(instance)
    known = {entity.__name__: entity for entity in entities}
    batches = []
    for item in configuration.load().initial_data:
        entity = known[item.entity]
        batches.append((entity, [_values(entity, record) for record in item.records]))
    inserted = engine.insert_missing(connection, batches)
    total = sum(len(item.records) for item in configuration.load().initial_data)
    return SetupResult(
        command="insert_initial_data",
        instance=member,
        success=True,
        affected=inserted,
        message=f"{inserted} of {total} Initial Data records inserted",
    )
