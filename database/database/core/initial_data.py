"""The Insert Initial Data Setup Operation: the configured Initial Data, inserted repeatably and unchanged."""

from datetime import date, datetime, time
from decimal import Decimal
from typing import Any
from uuid import UUID

from model.interface import entities

from database.core.configuration import CONFIGURATION, database_instance
from database.core.data import engine_for
from database.core.errors import (
    ConfigurationError,
    ExecutionError,
    InvalidInputError,
    SetupError,
)
from database.core.values import CheckedOrder, FilterCombination, SetupResult

_PARSERS = {
    "float": float,
    "decimal": lambda value: Decimal(str(value)),
    "datetime": datetime.fromisoformat,
    "date": date.fromisoformat,
    "time": time.fromisoformat,
    "uuid": UUID,
}


def _convert(entity: Any, record: dict[str, Any]) -> dict[str, Any]:
    """Return the record's values in the Python forms of the Entity's declared Types."""
    declared = {field.name: field.type.value for field in entity.declaration.fields}
    values = {}
    for name, value in record.items():
        if name not in declared:
            raise InvalidInputError(
                f"An Initial Data record of {entity.__name__} names an unknown Field."
            )
        parse = _PARSERS.get(declared[name])
        try:
            values[name] = (
                value
                if parse is None
                or value is None
                or not isinstance(value, int | float | str)
                else parse(value)
            )
        except ValueError, ArithmeticError:
            raise InvalidInputError(
                f"An Initial Data value of {entity.__name__} does not fit its Field."
            ) from None
    return values


def _stored(item: Any) -> dict[str, Any]:
    return {
        field.name: getattr(item, field.name)
        for field in type(item).declaration.fields
        if field.value_generation is None
    }


def insert_initial_data(selection: Any = None) -> SetupResult:
    """Insert every missing configured record, skip identical ones, and fail on a conflicting one."""
    instance, engine = engine_for(selection)
    by_name = {entity.__name__: entity for entity in entities}
    plan: list[tuple[Any, dict[str, Any]]] = []
    present: dict[Any, list[dict[str, Any]]] = {}
    processed = skipped = 0
    for group in CONFIGURATION.initial_data:
        entity: Any = by_name.get(group.entity)
        if entity is None:
            raise ConfigurationError(
                f"The Initial Data names {group.entity}, which is not an Entity of the Model."
            )
        if entity not in present:
            order = (CheckedOrder("id", "integer", False),)
            present[entity] = [
                {
                    key: value
                    for key, value in row.items()
                    if key in _stored_names(entity)
                }
                for row in engine.list(entity, (), FilterCombination.AND, order, -1)
            ]
        for record in group.records:
            processed += 1
            try:
                wanted = _stored(entity(**_convert(entity, record)))
            except ValueError:
                raise InvalidInputError(
                    f"An Initial Data record of {entity.__name__} does not satisfy its Entity contract."
                ) from None
            if wanted in present[entity]:
                skipped += 1
                continue
            keys = [entry for entry in entity.declaration.unique_constraints]
            if any(
                all(row[name] == wanted[name] for name in entry)
                for entry in keys
                for row in present[entity]
            ):
                raise SetupError(
                    f"An Initial Data record of {entity.__name__} conflicts with an existing record."
                )
            present[entity].append(wanted)
            plan.append((entity, wanted))
    try:
        inserted = engine.insert_records(plan) if plan else 0
    except ExecutionError as error:
        raise SetupError(
            f"Inserting the Initial Data did not complete: {error}"
        ) from None
    return SetupResult(
        "insert_initial_data",
        database_instance(instance.key),
        True,
        processed,
        f"Inserted {inserted} records; {skipped} already present.",
    )


def _stored_names(entity: Any) -> set[str]:
    return {
        field.name
        for field in entity.declaration.fields
        if field.value_generation is None
    }
