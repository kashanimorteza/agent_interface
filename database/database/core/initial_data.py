"""Initial Data: validating and inserting the shared Initial Data collection."""

import json
from typing import Any

import model

from .data import Selected, configuration
from .errors import ExecutionError, InvalidInputError
from .values import FilterCombination


def validate() -> list[tuple[Any, Any, int]]:
    """Build every Initial Data record through its Entity's own construction and return the Entities.

    A record that does not satisfy its Entity is reported by Entity and position, never repaired and never echoed.
    """
    entities = {entity.__name__: entity for entity in model.entities}
    prepared: list[tuple[Any, Any, int]] = []
    for block in configuration().initial_data:
        cls = entities.get(block.entity)
        if cls is None:
            raise InvalidInputError(
                f"Initial Data names the unknown Entity {block.entity!r}"
            )
        for position, record in enumerate(block.records, start=1):
            try:
                prepared.append((cls, cls.from_json(json.dumps(record)), position))
            except ValueError, TypeError:
                raise InvalidInputError(
                    f"Initial Data record {position} of {block.entity} does not satisfy its Entity"
                ) from None
    return prepared


def _values(cls: Any, entity: Any) -> dict[str, Any]:
    identity = cls.declaration.primary_key
    return {
        name: getattr(entity, name)
        for name in cls.model_fields
        if not (name == identity and getattr(entity, name) is None)
    }


def _identical(candidate: dict[str, Any], row: dict[str, Any]) -> bool:
    return all(row[name] == value for name, value in candidate.items())


def _conflicts(cls: Any, candidate: dict[str, Any], rows: list[dict[str, Any]]) -> bool:
    return any(
        all(row[name] == candidate[name] for name in constraint.fields)
        for constraint in cls.declaration.unique_constraints
        for row in rows
    )


def insert(selected: Selected) -> tuple[int, int]:
    """Insert every missing Initial Data record on the selected Instance in one atomic unit.

    A present identical record is skipped and a conflicting record fails the whole command without any change.
    Returns how many records were inserted and how many were already present.
    """
    prepared = validate()
    inserted = skipped = 0
    unit = selected.unit
    with unit.scope(selected.connection) as session:
        stored: dict[Any, list[dict[str, Any]]] = {}
        for cls, entity, position in prepared:
            if cls not in stored:
                stored[cls] = unit.list_rows(
                    session, cls, (), FilterCombination.AND, (), -1
                )
            rows = stored[cls]
            candidate = _values(cls, entity)
            if any(_identical(candidate, row) for row in rows):
                skipped += 1
                continue
            if _conflicts(cls, candidate, rows):
                raise ExecutionError(
                    f"Initial Data record {position} of {cls.__name__} conflicts with an existing record"
                )
            rows.append(unit.add(session, cls, candidate))
            inserted += 1
    return inserted, skipped
