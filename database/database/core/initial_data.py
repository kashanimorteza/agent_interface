"""Core Initial Data: coordinates the InsertInitialData Lifecycle Command and the Prepare command that follows CreateTables with it."""

import json
from collections.abc import Mapping
from enum import Enum
from typing import Any

from sqlmodel import SQLModel

from database.core import data, tables

type Prepared = tuple[tuple[type[SQLModel], Mapping[str, Any], SQLModel], ...]


def validated_records() -> Prepared:
    """Build every configured Initial Data record through its Entity's own contract, before anything is inserted.

    A record the Entity refuses fails the whole command, naming the Entity and the record's position.
    """
    entities = {entity.__name__: entity for entity in data.entity_collection}
    prepared: list[tuple[type[SQLModel], Mapping[str, Any], SQLModel]] = []
    for entry in data.configuration.initial_data:
        entity = entities.get(entry.entity)
        if entity is None:
            raise data.InvalidInputError(
                f"Initial Data names '{entry.entity}', which is not an Entity of the Model."
            )
        for position, record in enumerate(entry.records, start=1):
            try:
                built = data.entity_from_json(entity, json.dumps(record))
            except ValueError, TypeError:
                raise data.InvalidInputError(
                    f"Initial Data record {position} of Entity '{entry.entity}' does not satisfy the Entity contract."
                ) from None
            prepared.append((entity, record, built))
    return tuple(prepared)


def _relation_order() -> dict[type[SQLModel], int]:
    """Position of every Entity so that an Entity follows the Entities its Relations point to."""
    by_name = {
        data.declaration_of(entity).name: entity for entity in data.entity_collection
    }
    order: dict[type[SQLModel], int] = {}
    pending = list(data.entity_collection)
    while pending:
        for entity in pending:
            targets = [
                by_name[item.target_entity]
                for item in data.declaration_of(entity).relations
            ]
            if all(target in order or target is entity for target in targets):
                order[entity] = len(order)
                pending.remove(entity)
                break
        else:
            raise data.ConfigurationError(
                "The Entity Relations form a cycle, so no insertion order exists."
            )
    return order


def insert_initial_data(instance: Enum | None = None) -> data.LifecycleResult:
    """Insert every configured Initial Data record that is not already stored in the selected Instance."""
    prepared = validated_records()
    spec = data.resolve_instance(instance)
    unit, handle = data.connection_for(spec)
    order = _relation_order()
    ordered = sorted(prepared, key=lambda item: order[item[0]])
    records = [
        (
            entity,
            {name: getattr(built, name) for name in record},
            data.stored_values(built),
        )
        for entity, record, built in ordered
    ]
    inserted = unit.insert_missing(handle, records)
    return data.LifecycleResult(
        "insert_initial_data",
        data.instance_member(spec),
        True,
        len(records),
        f"{inserted} of {len(records)} records inserted.",
    )


def prepare(instance: Enum | None = None) -> data.LifecycleResult:
    """Run CreateTables and then InsertInitialData on the selected Instance; stop when CreateTables fails."""
    created = tables.create_tables(instance)
    inserted = insert_initial_data(instance)
    return data.LifecycleResult(
        "prepare",
        inserted.instance,
        True,
        (created.affected or 0) + (inserted.affected or 0),
        f"{created.message} {inserted.message}",
    )
