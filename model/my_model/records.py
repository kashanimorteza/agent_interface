"""The records the project must contain when it begins.

Each record is declared with the entity it belongs to. This module gathers them,
resolves the references between them, and gives the order in which they can be
read without meeting a reference to something that is not there yet.

A reference in a declared record identifies a record of the entity it points at
by that record's position among the entity's declarations, counting from one.
Positions are what a declaration can state; the identifiers themselves are
assigned by whichever layer stores the records.
"""

from __future__ import annotations

from .entities import ENTITIES
from .foundation import Entity, InitialRecord

FIRST_POSITION = 1


def declared_records() -> dict[str, tuple[InitialRecord, ...]]:
    """Every declared record, keyed by the entity that declares it."""

    return {
        entity.entity_name: entity.declared_records()
        for entity in ENTITIES
        if entity.declared_records()
    }


def entities_with_records() -> tuple[type[Entity], ...]:
    """The entities that declare at least one starting record."""

    return tuple(entity for entity in ENTITIES if entity.declared_records())


def _entity_by_name() -> dict[str, type[Entity]]:
    return {entity.entity_name: entity for entity in ENTITIES}


def referenced_entities(entity: type[Entity]) -> dict[str, type[Entity]]:
    """The entities this one points at, keyed by the field carrying the reference."""

    known = _entity_by_name()
    return {
        field_name: known[relationship.target]
        for field_name, relationship in entity.relationship_fields().items()
        if relationship.target in known
    }


def references_of(entity: type[Entity], record: InitialRecord) -> dict[str, type[Entity]]:
    """The references one declared record actually carries."""

    return {
        field_name: target
        for field_name, target in referenced_entities(entity).items()
        if field_name in record.values
    }


def unresolved_references() -> list[str]:
    """Every reference in a declared record that points at nothing declared."""

    complaints: list[str] = []
    for entity in entities_with_records():
        for position, record in enumerate(entity.declared_records(), start=FIRST_POSITION):
            for field_name, target in references_of(entity, record).items():
                pointed_at = record.values[field_name]
                available = len(target.declared_records())
                if not isinstance(pointed_at, int) or not (
                    FIRST_POSITION <= pointed_at <= available
                ):
                    complaints.append(
                        f"{entity.entity_name} record {position}: {field_name}="
                        f"{pointed_at!r} identifies no declared {target.entity_name}"
                    )
    return complaints


def resolution_order() -> tuple[type[Entity], ...]:
    """The record-declaring entities, each after everything its records point at."""

    remaining = list(entities_with_records())
    ordered: list[type[Entity]] = []
    placed: set[str] = set()

    while remaining:
        ready = [
            entity
            for entity in remaining
            if all(
                target.entity_name in placed or target is entity
                for target in referenced_entities(entity).values()
                if target.declared_records()
            )
        ]
        if not ready:
            unplaced = ", ".join(entity.entity_name for entity in remaining)
            raise ValueError(f"declared records reference each other in a cycle: {unplaced}")
        for entity in ready:
            ordered.append(entity)
            placed.add(entity.entity_name)
            remaining.remove(entity)

    return tuple(ordered)


def records_in_resolution_order() -> tuple[tuple[type[Entity], InitialRecord], ...]:
    """Every declared record, in an order where each reference is already available."""

    return tuple(
        (entity, record)
        for entity in resolution_order()
        for record in entity.declared_records()
    )
