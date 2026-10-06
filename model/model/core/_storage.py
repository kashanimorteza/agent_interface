"""Private storage mapping shared by every Entity: physical names, constraints, and identity.

Every Entity takes the same deterministic physical form: a table named exactly as the Entity's
physical name, columns named exactly as its Fields, constraints and indexes named by one
convention, and a generated identity column for an Auto Increment Field.
"""

import keyword
import re
import uuid
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import DateTime, Dialect, Identity, Index, String, TypeDecorator, UniqueConstraint
from sqlmodel import Field, SQLModel

from model.core.declaration import Declaration, FieldType, ValueGeneration

# One naming convention on the shared metadata names every constraint and index.
SQLModel.metadata.naming_convention = {
    "pk": "pk_%(table_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ix": "ix_%(table_name)s_%(column_0_N_name)s",
}

_FIELD_NAME = re.compile(r"[a-z][a-z0-9_]*")


class DecimalText(TypeDecorator[Decimal]):
    """Stores an exact decimal as its text and returns decimal.Decimal on every Engine."""

    impl = String
    cache_ok = True

    def process_bind_param(self, value: Decimal | None, dialect: Dialect) -> str | None:
        return None if value is None else str(value)

    def process_result_value(self, value: str | None, dialect: Dialect) -> Decimal | None:
        return None if value is None else Decimal(value)


class UTCDateTime(TypeDecorator[datetime]):
    """Stores a timezone-aware datetime in UTC; an Engine that drops the offset reads back UTC."""

    impl = DateTime(timezone=True)
    cache_ok = True

    def process_bind_param(self, value: datetime | None, dialect: Dialect) -> datetime | None:
        return None if value is None else value.astimezone(UTC)

    def process_result_value(self, value: datetime | None, dialect: Dialect) -> datetime | None:
        if value is None:
            return None
        return value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)


def physical_name(logical_name: str) -> str:
    """Return the PascalCase physical name of an Entity, or fail when none resolves."""
    parts = [part for part in re.split(r"[\s_\-]+", logical_name) if part]
    name = "".join(part[0].upper() + part[1:] for part in parts)
    if not name.isidentifier() or keyword.iskeyword(name):
        raise ValueError(f"Entity {logical_name}: no valid physical name")
    return name


def physical_field_name(logical_name: str) -> str:
    """Return the snake_case physical name of a Field, or fail when none resolves."""
    if not _FIELD_NAME.fullmatch(logical_name) or keyword.iskeyword(logical_name):
        raise ValueError(f"Field {logical_name}: no valid physical name")
    return logical_name


def table_args(declaration: Declaration) -> tuple[Any, ...]:
    """Return the table-level storage arguments of an Entity.

    Single-Field uniqueness and indexes are carried by the Field itself; only combinations of
    Fields are table-level. The generated-identity table option comes last, as a mapping.
    """
    args: list[Any] = [
        UniqueConstraint(*[physical_field_name(name) for name in unique.fields])
        for unique in declaration.unique_constraints
        if len(unique.fields) > 1
    ]
    args += [
        Index(None, *[physical_field_name(name) for name in index.fields])
        for index in declaration.indexes
        if len(index.fields) > 1
    ]
    if any(f.value_generation is ValueGeneration.auto_increment for f in declaration.fields):
        args.append({"sqlite_autoincrement": True})
    return tuple(args)


def column(declaration: Declaration, name: str) -> Any:
    """Return the Field definition of one declared Field, taken entirely from its Declaration."""
    field = next(f for f in declaration.fields if f.name == name)
    options: dict[str, Any] = {
        "nullable": field.nullable,
        "description": field.description,
    }
    if field.has_default:
        options["default"] = field.default
    elif field.value_generation is ValueGeneration.generated_identifier:
        options["default_factory"] = (
            uuid.uuid4 if field.type is FieldType.uuid else lambda: str(uuid.uuid4())
        )
    elif field.nullable or field.value_generation is not None:
        options["default"] = None
    if field.constraints.size is not None:
        options["max_length"] = field.constraints.size
    if field.type is FieldType.decimal:
        options["sa_type"] = DecimalText
    elif field.type is FieldType.datetime:
        options["sa_type"] = UTCDateTime
    if declaration.primary_key == name:
        options["primary_key"] = True
    if any(u.fields == (name,) for u in declaration.unique_constraints):
        options["unique"] = True
    if any(i.fields == (name,) for i in declaration.indexes):
        options["index"] = True
    for relation in declaration.relations:
        if relation.local_field == name:
            target = physical_name(relation.target_entity)
            options["foreign_key"] = f"{target}.{physical_field_name(relation.target_field)}"
    if field.value_generation is ValueGeneration.auto_increment:
        options["sa_column_args"] = [Identity()]
    physical_field_name(name)
    return Field(**options)
