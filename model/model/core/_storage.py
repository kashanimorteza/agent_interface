"""Storage-ready form shared by every Entity: deterministic names and exact value columns."""

from decimal import Decimal
from typing import Any, Final

from sqlalchemy import String, TypeDecorator, UniqueConstraint
from sqlmodel import SQLModel

NAMING_CONVENTION: Final = {
    "pk": "pk_%(table_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ix": "ix_%(table_name)s_%(column_0_N_name)s",
}

SQLModel.metadata.naming_convention = NAMING_CONVENTION


class DecimalText(TypeDecorator[Decimal]):
    """Stores the exact decimal text and returns decimal.Decimal on every Engine."""

    impl = String
    cache_ok = True

    def process_bind_param(self, value: Decimal | None, dialect: Any) -> str | None:
        return None if value is None else format(value, "f")

    def process_result_value(self, value: str | None, dialect: Any) -> Decimal | None:
        return None if value is None else Decimal(value)


def table_arguments(*unique_groups: tuple[str, ...]) -> tuple[Any, ...]:
    """Table arguments: combined uniqueness constraints, and an Identity column that auto-increments on SQLite."""
    return (
        *(UniqueConstraint(*group) for group in unique_groups),
        {"sqlite_autoincrement": True},
    )
