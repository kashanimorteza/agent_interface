"""The storage mapping form every Entity takes: names, identity, and exact values."""

from decimal import Decimal
from typing import Any

from sqlalchemy import Dialect, Identity, Index, String, UniqueConstraint
from sqlalchemy.types import TypeDecorator
from sqlmodel import SQLModel

from model.core.declaration import Declaration
from model.core.naming import entity_name, field_name

NAMING_CONVENTION = {
    "pk": "pk_%(table_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ix": "ix_%(table_name)s_%(column_0_N_name)s",
}

SQLModel.metadata.naming_convention = NAMING_CONVENTION


class DecimalText(TypeDecorator[Decimal]):
    """Stores the exact decimal text and returns a Decimal on every engine."""

    impl = String
    cache_ok = True

    def process_bind_param(self, value: Decimal | None, dialect: Dialect) -> str | None:
        return None if value is None else str(value)

    def process_result_value(
        self, value: str | None, dialect: Dialect
    ) -> Decimal | None:
        return None if value is None else Decimal(value)


def column_options(declaration: Declaration, name: str) -> dict[str, Any]:
    """Return the storage options of one Field, copied from its Entity's Declaration."""
    field = next(field for field in declaration.fields if field.name == name)
    options: dict[str, Any] = {}
    if declaration.primary_key == name:
        options["primary_key"] = True
    if field.value_generation == "auto_increment":
        options["sa_column_args"] = (Identity(),)
    if (name,) in declaration.unique_constraints:
        options["unique"] = True
    if (name,) in declaration.indexes:
        options["index"] = True
    for relation in declaration.relations:
        if relation.local_field == name:
            target = entity_name(relation.target_entity)
            options["foreign_key"] = f"{target}.{field_name(relation.target_field)}"
    if field.type == "decimal":
        options["sa_type"] = DecimalText
    return options


def table_args(declaration: Declaration) -> tuple[Any, ...]:
    """Return the table-level storage of one Entity: combined constraints and options."""
    args: list[Any] = []
    for names in declaration.unique_constraints:
        if len(names) > 1:
            args.append(UniqueConstraint(*(field_name(name) for name in names)))
    for names in declaration.indexes:
        if len(names) > 1:
            args.append(Index(None, *(field_name(name) for name in names)))
    if any(field.value_generation == "auto_increment" for field in declaration.fields):
        args.append({"sqlite_autoincrement": True})
    return tuple(args)
