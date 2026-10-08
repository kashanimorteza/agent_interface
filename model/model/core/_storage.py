"""Storage Mapping (private): the table-ready form derived only from a Declaration."""

import keyword
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any
from uuid import uuid4

from sqlalchemy import (
    DateTime,
    Dialect,
    Identity,
    Index,
    MetaData,
    String,
    TypeDecorator,
    UniqueConstraint,
)
from sqlalchemy.orm import registry
from sqlmodel import Field

from model.core._types import FieldType
from model.core.declaration import ABSENT, Declaration, ValueGeneration

NAMING_CONVENTION = {
    "pk": "pk_%(table_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ix": "ix_%(table_name)s_%(column_0_N_name)s",
}

ENTITY_REGISTRY = registry(metadata=MetaData(naming_convention=NAMING_CONVENTION))
"""The one registry whose table metadata holds every Entity's Table and no other."""


class _ExactDecimal(TypeDecorator[Decimal]):
    """Stores a decimal as its exact text on every Engine."""

    impl = String
    cache_ok = True

    def process_bind_param(self, value: Decimal | None, dialect: Dialect) -> str | None:
        return None if value is None else str(value)

    def process_result_value(
        self, value: str | None, dialect: Dialect
    ) -> Decimal | None:
        return None if value is None else Decimal(value)


class _UtcDateTime(TypeDecorator[datetime]):
    """Stores a datetime in UTC and reads it back timezone-aware."""

    impl = DateTime(timezone=True)
    cache_ok = True

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
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value.astimezone(UTC)


def physical_name(logical_name: str) -> str:
    """Return the deterministic physical name of a logical Entity name."""
    name = "".join(word[:1].upper() + word[1:] for word in logical_name.split())
    if not name.isidentifier() or keyword.iskeyword(name):
        raise ValueError(f"Entity name {logical_name!r} has no physical name")
    return name


def _identifier_factory(field_type: FieldType) -> Any:
    return uuid4 if field_type is FieldType.uuid else lambda: str(uuid4())


def field(declaration: Declaration, name: str) -> Any:
    """Return the table Field of one Field of the Declaration."""
    spec = next((item for item in declaration.fields if item.name == name), None)
    if spec is None:
        raise ValueError(f"Entity {declaration.name!r} declares no Field {name!r}")
    options: dict[str, Any] = {
        "nullable": spec.nullable,
        "description": spec.description,
        "repr": spec.sensitivity is None,
        "primary_key": name == declaration.primary_key,
        "unique": (name,) in declaration.unique_constraints,
        "index": (name,) in declaration.indexes,
    }
    match spec.value_generation:
        case ValueGeneration.auto_increment:
            options["default"] = None
            options["sa_column_args"] = (Identity(),)
        case ValueGeneration.generated_identifier:
            options["default_factory"] = _identifier_factory(spec.type)
        case None if spec.default is not ABSENT:
            options["default"] = spec.default
        case None if spec.nullable:
            options["default"] = None
    if spec.constraints.size is not None:
        options["max_length"] = spec.constraints.size
    relation = next(
        (item for item in declaration.relations if item.local_field == name), None
    )
    if relation is not None:
        target = physical_name(relation.target_entity)
        options["foreign_key"] = f"{target}.{relation.target_field}"
    if spec.type is FieldType.decimal:
        options["sa_type"] = _ExactDecimal
    elif spec.type is FieldType.datetime:
        options["sa_type"] = _UtcDateTime
    return Field(**options)


def table_args(declaration: Declaration) -> tuple[Any, ...]:
    """Return the table-level constraints and options of the Declaration."""
    args: list[Any] = [
        UniqueConstraint(*columns)
        for columns in declaration.unique_constraints
        if len(columns) > 1
    ]
    args += [
        Index(None, *columns) for columns in declaration.indexes if len(columns) > 1
    ]
    if any(
        item.value_generation is ValueGeneration.auto_increment
        for item in declaration.fields
    ):
        args.append({"sqlite_autoincrement": True})
    return tuple(args)
