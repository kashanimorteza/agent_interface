"""Private Storage Mapping: the table-ready form of an Entity, derived only from its Declaration."""

from typing import Any

from sqlalchemy import Identity, Index, UniqueConstraint
from sqlmodel import Field

from model.core import _types
from model.core._base import Base, physical_name
from model.core.declaration import NO_DEFAULT, Declaration, ValueGeneration

NAMING_CONVENTION = {
    "pk": "pk_%(table_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ix": "ix_%(table_name)s_%(column_0_N_name)s",
}

Base.metadata.naming_convention = NAMING_CONVENTION


def realize_field(declaration: Declaration, name: str) -> Any:
    """Return the column-level realization of one Field, taken from its Field Declaration and Entity Metadata."""
    field = next(item for item in declaration.fields if item.name == name)
    options: dict[str, Any] = {
        "nullable": field.nullable,
        "primary_key": name == declaration.primary_key,
    }
    if field.description is not None:
        options["description"] = field.description
    if field.default is not NO_DEFAULT:
        options["default"] = field.default
    elif field.nullable or field.value_generation is ValueGeneration.auto_increment:
        options["default"] = None
    if (name,) in declaration.unique_constraints:
        options["unique"] = True
    if (name,) in declaration.indexes:
        options["index"] = True
    relation = next(
        (item for item in declaration.relations if item.local_field == name), None
    )
    if relation is not None:
        options["foreign_key"] = (
            f"{physical_name(relation.target_entity)}.{relation.target_field}"
        )
    if field.constraints.size is not None:
        options["max_length"] = field.constraints.size
    column_type = _types.column_type(field.type)
    if column_type is not None:
        options["sa_type"] = column_type
    if field.value_generation is ValueGeneration.auto_increment:
        options["sa_column_args"] = [Identity()]
    return Field(**options)


def table_args(declaration: Declaration) -> tuple[Any, ...]:
    """Return the table-level realization: combined uniqueness, combined indexes and identity behaviour."""
    items: list[Any] = [
        UniqueConstraint(*entry)
        for entry in declaration.unique_constraints
        if len(entry) > 1
    ]
    items += [Index(None, *entry) for entry in declaration.indexes if len(entry) > 1]
    if any(
        field.value_generation is ValueGeneration.auto_increment
        for field in declaration.fields
    ):
        items.append({"sqlite_autoincrement": True})
    return tuple(items)
