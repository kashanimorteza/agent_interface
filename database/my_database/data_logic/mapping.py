"""The shared definitions, expressed as stored structure.

Every persistent definition becomes one table; its resolved fields become that
table's columns; its declared connections become explicit references; and the
rules it declared but could not judge on its own become constraints that hold
when changes are committed. Each table records which definition it implements,
so the two can always be compared.

Nothing here decides what the domain means. It decides only how that meaning is
held, in terms that belong to no particular engine.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from my_model import ENTITIES, Cardinality, Entity, FieldSpec, FieldType, RuleScope, is_stated
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    Numeric,
    String,
    Table,
    UniqueConstraint,
)

from . import naming

metadata = MetaData()

_COLUMN_TYPES = {
    FieldType.INTEGER: lambda spec: Integer(),
    FieldType.STRING: lambda spec: String(int(spec.size)) if is_stated(spec.size) else String(),
    FieldType.BOOLEAN: lambda spec: Boolean(),
    FieldType.DECIMAL: lambda spec: Numeric(),
    FieldType.FLOAT: lambda spec: Float(),
    FieldType.DATETIME: lambda spec: DateTime(),
}

PYTHON_TYPES = {
    FieldType.INTEGER: int,
    FieldType.STRING: str,
    FieldType.BOOLEAN: bool,
    FieldType.DECIMAL: Decimal,
    FieldType.FLOAT: float,
    FieldType.DATETIME: datetime,
}

# Physical choices for a reference the definitions did not make themselves.
REFERENCE_INDEXED = True
ON_DELETE = "RESTRICT"
ON_UPDATE = "RESTRICT"


def _column(entity: type[Entity], name: str, spec: FieldSpec) -> Column:
    primary_key = bool(is_stated(spec.primary_key) and spec.primary_key)
    nullable = bool(is_stated(spec.nullable) and spec.nullable)
    unique = bool(is_stated(spec.unique) and spec.unique)

    arguments: dict[str, object] = {
        "primary_key": primary_key,
        "nullable": nullable if not primary_key else False,
        "comment": str(spec.purpose) if is_stated(spec.purpose) else None,
    }
    if primary_key:
        arguments["autoincrement"] = bool(is_stated(spec.auto_increment) and spec.auto_increment)
    if unique and not primary_key:
        arguments["unique"] = True
    if is_stated(spec.default) and not primary_key:
        arguments["default"] = spec.default

    reference = entity.relationship_fields().get(name)
    if reference is None:
        return Column(name, _COLUMN_TYPES[spec.type](spec), **arguments)

    target = _entity_named(reference.target)
    target_key = _primary_key_name(target)
    # The reference carries the same type as the key it points at, and its
    # optionality is the one the definitions resolved, not a default of ours.
    return Column(
        name,
        _COLUMN_TYPES[target.entity_fields[target_key].type](target.entity_fields[target_key]),
        ForeignKey(
            f"{naming.table_name(target.entity_name)}.{target_key}",
            ondelete=ON_DELETE,
            onupdate=ON_UPDATE,
            name=f"fk_{naming.table_name(entity.entity_name)}_{name}",
        ),
        index=REFERENCE_INDEXED,
        **arguments,
    )


def _entity_named(name: str) -> type[Entity]:
    for entity in ENTITIES:
        if entity.entity_name == name:
            return entity
    raise KeyError(f"no published definition is named {name!r}")


def _primary_key_name(entity: type[Entity]) -> str:
    for name, spec in entity.entity_fields.items():
        if is_stated(spec.primary_key) and spec.primary_key:
            return name
    raise KeyError(f"{entity.entity_name} declares no identifying field")


def _stored_state_constraints(entity: type[Entity]) -> list[UniqueConstraint]:
    """The declared rules this layer is the first able to enforce."""

    constraints: list[UniqueConstraint] = []
    table = naming.table_name(entity.entity_name)
    for rule in entity.rules_for(RuleScope.STORED_STATE):
        if len(rule.fields) < 2:
            continue
        constraints.append(
            UniqueConstraint(
                *rule.fields,
                name=naming.unique_constraint_name(table, tuple(rule.fields)),
                comment=rule.statement,
            )
        )
    return constraints


def build() -> dict[str, Table]:
    """One table for every published definition, keyed by definition name."""

    tables: dict[str, Table] = {}
    for entity in ENTITIES:
        name = naming.table_name(entity.entity_name)
        table = Table(
            name,
            metadata,
            *(
                _column(entity, field_name, spec)
                for field_name, spec in entity.entity_fields.items()
            ),
            *_stored_state_constraints(entity),
            comment=f"Implements the {entity.entity_name} definition.",
            info={"definition": entity.entity_name},
        )
        tables[entity.entity_name] = table
    return tables


TABLES: dict[str, Table] = build()


def table_for(entity: type[Entity]) -> Table:
    """The table one definition is held in."""

    try:
        return TABLES[entity.entity_name]
    except KeyError:
        raise KeyError(f"{entity.entity_name} has no stored structure") from None


def definition_of(table: Table) -> type[Entity]:
    """The definition a table implements."""

    return _entity_named(table.info["definition"])


def identifying_field(entity: type[Entity]) -> str:
    return _primary_key_name(entity)


def unique_fields(entity: type[Entity]) -> tuple[str, ...]:
    """The fields declared unique on their own, which name a record."""

    return tuple(
        name
        for name, spec in entity.entity_fields.items()
        if is_stated(spec.unique)
        and spec.unique
        and not (is_stated(spec.primary_key) and spec.primary_key)
    )


def natural_key(entity: type[Entity]) -> tuple[str, ...]:
    """The fields that say which logical record this is, apart from its key.

    A field declared unique on its own is enough; otherwise the fields a
    declared multi-field uniqueness rule names together are what identify it.
    """

    single = unique_fields(entity)
    if single:
        return single[:1]
    for rule in entity.rules_for(RuleScope.STORED_STATE):
        if len(rule.fields) >= 2:
            return tuple(rule.fields)
    return ()


def entity_named(name: str) -> type[Entity]:
    return _entity_named(name)


__all__ = [
    "ON_DELETE",
    "ON_UPDATE",
    "PYTHON_TYPES",
    "REFERENCE_INDEXED",
    "TABLES",
    "definition_of",
    "entity_named",
    "identifying_field",
    "metadata",
    "natural_key",
    "table_for",
    "unique_fields",
]
