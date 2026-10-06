"""Core Initial Data: coordinates the InsertInitialData Lifecycle Command.

Every configured record is validated through its Entity's public contract and inserted unchanged.
A record that is already present and identical is skipped, a conflicting record fails clearly, and
nothing is overwritten, deleted, or duplicated.
"""

import json
from typing import Any

from model.interface import entities as _entities
from pydantic import ValidationError

from database.core.data import Data
from database.core.errors import ConfigurationError
from database.core.values import DatabaseInstance, LifecycleResult

COMMAND = "insert_initial_data"


def _entity_for(name: str) -> Any:
    for entity_cls in _entities:
        if entity_cls.__name__ == name:
            return entity_cls
    raise ConfigurationError(f"Initial Data names {name}, which Model does not publish")


def _values(entity_cls: Any, record: dict[str, Any]) -> dict[str, Any]:
    """Validate a record through the Entity's own JSON contract and return its stored values."""
    entity = entity_cls.from_json(json.dumps(record))
    generated = {
        f.name
        for f in entity_cls.declaration.fields
        if f.value_generation is not None and f.value_generation.value == "auto_increment"
    }
    return {
        f.name: getattr(entity, f.name)
        for f in entity_cls.declaration.fields
        if f.name not in generated
    }


def insert_initial_data(data: Data, instance: DatabaseInstance | None) -> LifecycleResult:
    selected = data.instance(instance)
    member = DatabaseInstance[selected.member]
    batch: list[tuple[Any, dict[str, Any]]] = []
    for group in data.configuration.initial_data:
        entity_cls = _entity_for(group.entity)
        for position, record in enumerate(group.records, start=1):
            try:
                batch.append((entity_cls, _values(entity_cls, record)))
            except ValidationError as error:
                fields = sorted(
                    {
                        str(item["loc"][0])
                        for item in error.errors(include_input=False)
                        if item["loc"]
                    }
                )
                message = (
                    f"Stopped, record {position} of {group.entity} breaks its Entity contract"
                    f" in: {', '.join(fields)}"
                )
                return LifecycleResult(COMMAND, member, False, None, message)
            except ValueError:
                message = f"Stopped, record {position} of {group.entity} is not valid"
                return LifecycleResult(COMMAND, member, False, None, message)
    outcome = data.engine(selected).insert_initial(batch)
    if outcome["conflict"] is not None:
        return LifecycleResult(COMMAND, member, False, None, f"Stopped, {outcome['conflict']}")
    inserted, skipped = outcome["inserted"], outcome["skipped"]
    message = f"Inserted {inserted} records; skipped {skipped} identical records"
    return LifecycleResult(COMMAND, member, True, inserted + skipped, message)
