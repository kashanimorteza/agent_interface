"""Private Storage Mapping: the table-ready form derived only from a Declaration."""

import decimal
import keyword
import uuid
from typing import Any, Final

from sqlalchemy import Identity, MetaData, String, TypeDecorator
from sqlalchemy import Index as TableIndex
from sqlalchemy import UniqueConstraint as TableUniqueConstraint
from sqlalchemy.engine import Dialect
from sqlalchemy.orm import registry
from sqlmodel import Field

from model.core.declaration import (
    NO_DEFAULT,
    Declaration,
    FieldDeclaration,
    FieldType,
    ValueGeneration,
)

NAMING_CONVENTION: Final = {
    "pk": "pk_%(table_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ix": "ix_%(table_name)s_%(column_0_N_name)s",
}

REGISTRY: Final = registry(metadata=MetaData(naming_convention=NAMING_CONVENTION))
"""The registry whose shared table metadata holds every Entity table and no other."""


class ExactDecimal(TypeDecorator[decimal.Decimal]):
    """Stores a decimal as its exact text and reads it back as a decimal on every Engine."""

    impl = String
    cache_ok = True

    def process_bind_param(
        self, value: decimal.Decimal | None, dialect: Dialect
    ) -> str | None:
        return None if value is None else str(value)

    def process_result_value(
        self, value: str | None, dialect: Dialect
    ) -> decimal.Decimal | None:
        return None if value is None else decimal.Decimal(value)


def physical_entity_name(logical_name: str) -> str:
    """The deterministic physical name of an Entity: its words in PascalCase."""
    words = logical_name.split(" ")
    physical = "".join(word[:1].upper() + word[1:] for word in words)
    if not all(words) or not physical.isidentifier() or keyword.iskeyword(physical):
        raise ValueError(f"Entity name {logical_name!r} has no valid physical name")
    return physical


def physical_field_name(logical_name: str) -> str:
    """The deterministic physical name of a Field: its snake_case logical name."""
    if (
        not logical_name.isidentifier()
        or keyword.iskeyword(logical_name)
        or logical_name != logical_name.lower()
    ):
        raise ValueError(f"Field name {logical_name!r} has no valid physical name")
    return logical_name


def _field(declaration: Declaration, name: str) -> FieldDeclaration:
    for field in declaration.fields:
        if field.name == name:
            return field
    raise ValueError(f"Entity {declaration.name!r} declares no Field {name!r}")


def _single(entries: tuple[Any, ...], name: str) -> bool:
    return any(entry.fields == (name,) for entry in entries)


def _generated_identifier(field: FieldDeclaration) -> Any:
    if field.type is FieldType.UUID:
        return uuid.uuid4
    return lambda: str(uuid.uuid4())


def mapped_field(declaration: Declaration, name: str) -> Any:
    """Realize one Field from its Field Declaration and its Entity's Metadata."""
    field = _field(declaration, name)
    options: dict[str, Any] = {
        "description": field.description,
        "nullable": field.nullable,
        "primary_key": name == declaration.primary_key,
        "unique": _single(declaration.unique_constraints, name),
        "index": _single(declaration.indexes, name),
    }
    for relation in declaration.relations:
        if relation.local_field == name:
            target = physical_entity_name(relation.target_entity)
            options["foreign_key"] = (
                f"{target}.{physical_field_name(relation.target_field)}"
            )
    if field.constraints.size is not None:
        options["max_length"] = field.constraints.size
    if field.type is FieldType.DECIMAL:
        options["sa_type"] = ExactDecimal
    if field.value_generation is ValueGeneration.AUTO_INCREMENT:
        options["sa_column_args"] = [Identity()]
        return Field(default=None, **options)
    if field.value_generation is ValueGeneration.GENERATED_IDENTIFIER:
        return Field(default_factory=_generated_identifier(field), **options)
    if field.default is not NO_DEFAULT:
        return Field(default=field.default, **options)
    if field.nullable:
        return Field(default=None, **options)
    return Field(**options)


def table_arguments(declaration: Declaration) -> tuple[Any, ...]:
    """The table-level constraints, indexes, and options of an Entity."""
    arguments: list[Any] = [
        TableUniqueConstraint(*entry.fields)
        for entry in declaration.unique_constraints
        if len(entry.fields) > 1
    ]
    arguments += [
        TableIndex(None, *entry.fields)
        for entry in declaration.indexes
        if len(entry.fields) > 1
    ]
    auto_increment = any(
        field.value_generation is ValueGeneration.AUTO_INCREMENT
        for field in declaration.fields
    )
    return (*arguments, {"sqlite_autoincrement": auto_increment})
