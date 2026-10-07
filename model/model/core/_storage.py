"""Storage Mapping: the private table-ready form of every Entity, derived only from its Declaration."""

import keyword
import re
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import DateTime, Identity, Index, MetaData, String, UniqueConstraint
from sqlalchemy.engine import Dialect
from sqlalchemy.orm import registry
from sqlalchemy.types import TypeDecorator
from sqlmodel import Field

from ._types import entity_physical_name
from .declaration import (
    ABSENT,
    Declaration,
    FieldDeclaration,
    FieldType,
    ValueGeneration,
)

NAMING_CONVENTION = {
    "pk": "pk_%(table_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ix": "ix_%(table_name)s_%(column_0_N_name)s",
}

# The one shared table metadata in which the table form of every Entity is registered.
REGISTRY = registry(metadata=MetaData(naming_convention=NAMING_CONVENTION))

_COLUMN_NAME = re.compile(r"[a-z][a-z0-9]*(_[a-z0-9]+)*")


def table_name(declaration: Declaration) -> str:
    """Return the table name of an Entity: its physical name."""
    return entity_physical_name(declaration.name)


def column_name(field: FieldDeclaration) -> str:
    """Return the column name of a Field: its Field name, or fail when it cannot be resolved."""
    if not _COLUMN_NAME.fullmatch(field.name) or keyword.iskeyword(field.name):
        raise ValueError(f"The Field name {field.name!r} has no valid column name")
    return field.name


class ExactDecimal(TypeDecorator[Decimal]):
    """Stores a decimal as its exact text and returns it as a decimal on every Engine."""

    impl = String
    cache_ok = True

    def process_bind_param(self, value: Decimal | None, dialect: Dialect) -> str | None:
        return None if value is None else str(value)

    def process_result_value(
        self, value: str | None, dialect: Dialect
    ) -> Decimal | None:
        return None if value is None else Decimal(value)


class UtcDateTime(TypeDecorator[datetime]):
    """Stores a datetime in UTC and returns it timezone-aware, even where the Engine drops the offset."""

    impl = DateTime
    cache_ok = True

    def __init__(self) -> None:
        super().__init__(timezone=True)

    def process_bind_param(
        self, value: datetime | None, dialect: Dialect
    ) -> datetime | None:
        if value is None:
            return None
        if value.utcoffset() is None:
            raise ValueError("A datetime must be timezone-aware")
        return value.astimezone(UTC)

    def process_result_value(
        self, value: datetime | None, dialect: Dialect
    ) -> datetime | None:
        if value is None:
            return None
        return (
            value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)
        )


def _single_entries(declaration: Declaration) -> tuple[set[str], set[str]]:
    unique = {
        entry.fields[0]
        for entry in declaration.unique_constraints
        if len(entry.fields) == 1
    }
    indexed = {
        entry.fields[0] for entry in declaration.indexes if len(entry.fields) == 1
    }
    return unique, indexed


def realize_field(declaration: Declaration, name: str) -> Any:
    """Return the table-ready Field for one declared Field, with its value rules and storage options."""
    item = next(candidate for candidate in declaration.fields if candidate.name == name)
    column_name(item)
    unique, indexed = _single_entries(declaration)
    shared = unique & indexed
    options: dict[str, Any] = {}

    if item.description is not None:
        options["description"] = item.description
    if item.constraints.size is not None:
        options["max_length"] = item.constraints.size

    if item.value_generation == ValueGeneration.auto_increment:
        options["default"] = None
        options["sa_column_args"] = (Identity(),)
    elif item.value_generation is None:
        if item.default is not ABSENT:
            options["default"] = item.default
        elif item.nullable:
            options["default"] = None

    if item.name == declaration.primary_key:
        options["primary_key"] = True
    for relation in declaration.relations:
        if relation.local_field == item.name:
            options["foreign_key"] = (
                f"{entity_physical_name(relation.target_entity)}.{relation.target_field}"
            )
    if item.name in unique - shared:
        options["unique"] = True
    if item.name in indexed - shared:
        options["index"] = True

    if item.type == FieldType.decimal:
        options["sa_type"] = ExactDecimal
    elif item.type == FieldType.datetime:
        options["sa_type"] = UtcDateTime
    return Field(**options)


def table_arguments(declaration: Declaration) -> tuple[Any, ...]:
    """Return the table-level storage arguments: combined uniqueness and indexes, and the identity setting."""
    unique, indexed = _single_entries(declaration)
    shared = unique & indexed
    arguments: list[Any] = [
        UniqueConstraint(*entry.fields)
        for entry in declaration.unique_constraints
        if len(entry.fields) > 1 or entry.fields[0] in shared
    ]
    arguments += [
        Index(None, *entry.fields)
        for entry in declaration.indexes
        if len(entry.fields) > 1 or entry.fields[0] in shared
    ]
    if any(
        item.value_generation == ValueGeneration.auto_increment
        for item in declaration.fields
    ):
        arguments.append({"sqlite_autoincrement": True})
    return tuple(arguments)
