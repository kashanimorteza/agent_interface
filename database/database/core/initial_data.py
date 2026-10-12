"""insert_initial_data: the configured Initial Data, inserted repeatably."""

import json
from typing import Any

from pydantic import ValidationError

from database.core.configuration import configuration
from database.core.data import resolve
from database.core.errors import DatabaseError
from database.core.values import SetupResult

COMMAND = "insert_initial_data"


def _auto_increment(declared: Any) -> bool:
    generation = declared.value_generation
    return generation is not None and generation.value == "auto_increment"


def _prepared(
    entity: Any, position: int, record: dict[str, Any], problems: list[str]
) -> dict[str, Any] | None:
    where = f"{entity.__name__} Initial Data record {position}"
    try:
        built = entity.from_json(json.dumps(record))
    except ValidationError as error:
        fields = sorted({".".join(map(str, item["loc"])) for item in error.errors()})
        problems.append(f"{where} breaks the Entity contract in {', '.join(fields)}")
        return None
    except TypeError, ValueError:
        problems.append(f"{where} holds a value outside its Field Types")
        return None
    return {
        declared.name: getattr(built, declared.name)
        for declared in entity.declaration.fields
        if not _auto_increment(declared)
    }


def insert_initial_data(instance: Any = None) -> SetupResult:
    """Insert every missing configured record, skip identical ones, fail on conflicts."""
    settings = configuration()
    member, resolved, unit = resolve(instance)
    problems: list[str] = []
    items: list[tuple[Any, int, dict[str, Any], tuple[str, ...], tuple[Any, ...]]] = []
    for group in settings.initial_data:
        entity: Any = group.entity
        keys = tuple(
            constraint.fields for constraint in entity.declaration.unique_constraints
        )
        for position, record in enumerate(group.records, start=1):
            values = _prepared(entity, position, dict(record), problems)
            if values is not None:
                given = tuple(name for name in record if name in values)
                usable = tuple(key for key in keys if set(key) <= set(given))
                items.append((entity, position, values, given, usable))
    if problems:
        return SetupResult(
            command=COMMAND,
            instance=member,
            success=False,
            affected=None,
            message="invalid Initial Data: " + "; ".join(problems),
        )
    try:
        inserted = unit.insert_initial_data(resolved, items)
    except DatabaseError as error:
        return SetupResult(
            command=COMMAND,
            instance=member,
            success=False,
            affected=None,
            message=str(error),
        )
    return SetupResult(
        command=COMMAND,
        instance=member,
        success=True,
        affected=inserted,
        message=(
            f"{inserted} Initial Data records inserted, "
            f"{len(items) - inserted} already present"
        ),
    )
