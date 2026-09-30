"""InsertInitialData: insert the shared Initial Data that is missing, repeatably."""

from collections.abc import Sequence
from typing import Any

from pydantic import ValidationError

from database.core import data
from database.core._cli import run
from database.core._contracts import DatabaseInstance, LifecycleResult
from database.core._entities import entity_classes
from database.core._failures import InvalidInputFailure, LifecycleFailure, sanitized


def _records() -> list[tuple[str, dict[str, Any]]]:
    """Every declared record, validated through its public Entity contract."""
    validated: list[tuple[str, dict[str, Any]]] = []
    classes = entity_classes()
    for item in data.configuration().initial_data:
        for position, record in enumerate(item.records, start=1):
            try:
                entity = classes[item.entity](**record)
            except ValidationError as error:
                fields = sorted(
                    {str(part) for problem in error.errors() for part in problem["loc"]}
                )
                raise InvalidInputFailure(
                    f"Initial Data record {position} of {item.entity} is invalid "
                    f"(Fields: {', '.join(fields)})."
                ) from None
            validated.append((item.entity, data.stored_values(item.entity, entity)))
    return validated


@sanitized
def insert_initial_data(instance: DatabaseInstance | None = None) -> LifecycleResult:
    """Insert missing shared Initial Data on the selected Instance; safe to repeat."""
    key = data.select_instance(instance)
    member = DatabaseInstance(key)
    records = _records()
    if not records:
        return LifecycleResult(
            "insert_initial_data", member, True, 0, "No Initial Data is declared."
        )
    engine = data.engine_for(key)
    missing = engine.missing_tables()
    if missing:
        raise LifecycleFailure(
            "Tables are missing on the Instance; run CreateTables first."
        )
    inserted = engine.insert_missing(records)
    return LifecycleResult(
        "insert_initial_data",
        member,
        True,
        inserted,
        f"{inserted} records inserted; {len(records) - inserted} were already present.",
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Manual entry point: invokes the public command and adds no logic of its own."""

    def command(instance: DatabaseInstance | None) -> LifecycleResult:
        from database.interface import Database

        return Database.insert_initial_data(instance)

    return run("Insert the shared Initial Data that is missing.", command, argv)
