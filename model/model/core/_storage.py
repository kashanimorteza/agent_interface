"""Private Storage Mapping: the table-ready form of every Entity, derived only from its Declaration.

Model declares this form and never runs storage.
"""

import keyword
import re
from decimal import Decimal
from typing import Any

from sqlalchemy import Identity, MetaData, String
from sqlalchemy import Index as TableIndex
from sqlalchemy import UniqueConstraint as TableUniqueConstraint
from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.orm import registry as sa_registry
from sqlalchemy.types import TypeDecorator
from sqlmodel import Field as ColumnField
from sqlmodel import SQLModel

from model.core import _types
from model.core.declaration import (
    EntityDeclaration,
    FieldDeclaration,
    FieldType,
    ValueGeneration,
)

_SNAKE_CASE = re.compile(r"^[a-z][a-z0-9]*(_[a-z0-9]+)*$")
_WORD = re.compile(r"^[A-Za-z][A-Za-z0-9]*$")

#: Names a Field cannot take because the Entity type already uses them.
RESERVED_FIELD_NAMES = frozenset(dir(SQLModel)) | {
    "declaration",
    "to_json",
    "from_json",
    "metadata",
    "registry",
}


class StorageMappingError(ValueError):
    """Raised when a name cannot be resolved into a table-ready form."""


def physical_name(logical_name: str) -> str:
    """The physical Entity name: each word of the logical name capitalized and joined."""
    words = logical_name.split()
    if not words or not all(_WORD.match(word) for word in words):
        raise StorageMappingError(
            f"Entity {logical_name!r}: the name cannot be resolved to a physical name."
        )
    name = "".join(word[0].upper() + word[1:] for word in words)
    if keyword.iskeyword(name):
        raise StorageMappingError(
            f"Entity {logical_name!r}: the physical name {name!r} is a reserved word."
        )
    return name


def table_name(declaration: EntityDeclaration) -> str:
    """The table name of an Entity: exactly its physical name."""
    return physical_name(declaration.name)


def column_name(entity: EntityDeclaration, field: FieldDeclaration) -> str:
    """The column name of a Field: exactly its Field name."""
    name = field.name
    if not _SNAKE_CASE.match(name):
        raise StorageMappingError(
            f"Entity {entity.name!r}: Field {name!r} is not a snake_case name."
        )
    if keyword.iskeyword(name) or name in RESERVED_FIELD_NAMES:
        raise StorageMappingError(
            f"Entity {entity.name!r}: Field {name!r} collides with a reserved word."
        )
    return name


def check_relations(declarations: tuple[EntityDeclaration, ...]) -> None:
    """Fail unless every Relation resolves to a Field of an Entity of the same set with a compatible Type."""
    by_name: dict[str, EntityDeclaration] = {}
    physical: dict[str, str] = {}
    for declaration in declarations:
        if (
            declaration.name in by_name
            or physical.setdefault(table_name(declaration), declaration.name)
            != declaration.name
        ):
            raise StorageMappingError(
                f"Entity {declaration.name!r}: the name is duplicated or collides after normalization."
            )
        by_name[declaration.name] = declaration
    for declaration in declarations:
        for relation in declaration.relations:
            target = by_name.get(relation.target_entity)
            if target is None or relation.target_field not in target.field_names:
                raise StorageMappingError(
                    f"Entity {declaration.name!r}: the Relation on {relation.local_field!r} does not resolve."
                )
            if (
                declaration.field(relation.local_field).type
                is not target.field(relation.target_field).type
            ):
                raise StorageMappingError(
                    f"Entity {declaration.name!r}: the Relation on {relation.local_field!r} joins incompatible Types."
                )


#: The one naming convention of every constraint and index.
NAMING_CONVENTION = {
    "pk": "pk_%(table_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ix": "ix_%(table_name)s_%(column_0_N_name)s",
}


#: The one shared table metadata in which every Entity's table form is registered.
METADATA = MetaData(naming_convention=NAMING_CONVENTION)
REGISTRY = sa_registry(metadata=METADATA)


class ExactDecimal(TypeDecorator[Decimal]):
    """Stores a decimal as its exact text and returns a decimal on every Engine."""

    impl = String
    cache_ok = True

    def process_bind_param(self, value: Decimal | None, dialect: Dialect) -> str | None:
        if value is None:
            return None
        if not isinstance(value, Decimal) or not value.is_finite():
            raise ValueError("Only a finite decimal can be stored.")
        return str(value)

    def process_result_value(
        self, value: str | None, dialect: Dialect
    ) -> Decimal | None:
        return None if value is None else Decimal(value)


def realize_field(entity: EntityDeclaration, field: FieldDeclaration | str) -> Any:
    """The table-ready Field of a Field Declaration, given or named.

    Value rules come from the Field Declaration; the Primary Key, uniqueness, index, and foreign key
    come from the Entity's Declaration, which stays their only source.
    """
    if isinstance(field, str):
        field = entity.field(field)
    column_name(entity, field)
    options: dict[str, Any] = {
        "description": field.description,
        "nullable": field.nullable,
    }
    if field.has_default:
        options["default"] = field.default
    elif field.value_generation is ValueGeneration.generated_identifier:
        options["default_factory"] = _types.identifier_factory(field.type)
    elif field.nullable or field.value_generation is ValueGeneration.auto_increment:
        options["default"] = None
    if field.constraints.size is not None:
        options["max_length"] = field.constraints.size
    if field.type is FieldType.decimal:
        options["sa_type"] = ExactDecimal
    if field.sensitivity is not None:
        options["repr"] = False
    if field.name == entity.primary_key:
        options["primary_key"] = True
    if any(c.fields == (field.name,) for c in entity.unique_constraints):
        options["unique"] = True
    if any(i.fields == (field.name,) for i in entity.indexes):
        options["index"] = True
    for relation in entity.relations:
        if relation.local_field == field.name:
            options["foreign_key"] = (
                f"{physical_name(relation.target_entity)}.{relation.target_field}"
            )
    if field.value_generation is ValueGeneration.auto_increment:
        options["sa_column_args"] = (Identity(),)
    return ColumnField(**options)


def table_args(entity: EntityDeclaration) -> tuple[Any, ...]:
    """The table-level uniqueness, indexes, and options of an Entity's table form.

    A single-Field entry is realized on its column; only a combination is realized here.
    """
    args: list[Any] = [
        TableUniqueConstraint(*c.fields)
        for c in entity.unique_constraints
        if len(c.fields) > 1
    ]
    args += [TableIndex(None, *i.fields) for i in entity.indexes if len(i.fields) > 1]
    options: dict[str, Any] = {}
    if any(f.value_generation is ValueGeneration.auto_increment for f in entity.fields):
        options["sqlite_autoincrement"] = True
    return (*args, options) if options else tuple(args)
