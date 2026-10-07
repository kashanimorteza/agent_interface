import json
from types import ModuleType
from typing import Any

from database.core.configuration import CONFIGURATION, Connection
from database.core.errors import ConfigurationError, ExecutionError, InvalidInputError
from database.core.tables import entity_named


def _prepare() -> list[tuple[type[Any], dict[str, Any]]]:
    """Validate every configured record through its Entity's public contract."""
    prepared = []
    for group in CONFIGURATION.initial_data:
        entity = entity_named(group.entity)
        if entity is None:
            raise ConfigurationError(f"The Initial Data names an unknown Entity: {group.entity}.")
        for position, record in enumerate(group.records, start=1):
            try:
                built = entity.from_json(json.dumps(record))
            except ValueError:
                raise InvalidInputError(
                    f"Initial Data record {position} of {entity.declaration.name} "
                    "does not satisfy the Entity contract."
                ) from None
            values = {
                field.name: getattr(built, field.name)
                for field in entity.declaration.fields
                if field.value_generation is None
            }
            prepared.append((entity, values))
    return prepared


def _criteria(entity: type[Any], values: dict[str, Any]) -> list[dict[str, Any]]:
    """The ways a stored record can be the same record: each uniqueness constraint."""
    found = []
    for constraint in entity.declaration.unique_constraints:
        if all(values[name] is not None for name in constraint.fields):
            found.append({name: values[name] for name in constraint.fields})
    return found or [values]


def insert_initial_data(unit: ModuleType, connection: Connection) -> tuple[int, int]:
    """Insert every missing configured record; return (inserted, processed).

    An identical stored record is skipped and a conflicting one fails everything.
    """
    prepared = _prepare()
    inserted = 0
    with unit.records(connection) as records:
        for entity, values in prepared:
            stored = [
                row
                for criteria in _criteria(entity, values)
                if (row := records.find(entity, criteria)) is not None
            ]
            identical = any(
                all(row[name] == value for name, value in values.items()) for row in stored
            )
            if identical:
                continue
            if stored:
                raise ExecutionError(
                    f"An Initial Data record of {entity.declaration.name} conflicts with a stored "
                    "record; nothing was inserted."
                )
            records.insert(entity, values)
            inserted += 1
    return inserted, len(prepared)
