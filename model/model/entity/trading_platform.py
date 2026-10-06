"""The Trading Platform Entity."""

from typing import ClassVar

from model.core._storage import column, table_args
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    UniqueConstraint,
    ValueGeneration,
)
from model.core.foundation import Foundation

_DECLARATION = Declaration(
    name="Trading Platform",
    description=(
        "Defines a supported trading API standard, such as MetaTrader 5 or "
        "Binance, while keeping the system independent of any specific "
        "exchange or broker. Every trading platform implementation exposes the "
        "same application-facing trading functions through a dedicated class, "
        "while handling communication with its destination API according to "
        "that platform's own mechanism. Additional platform implementations "
        "can be added without changing the system's common trading interface."
    ),
    fields=(
        FieldDeclaration(
            name="id",
            type=FieldType.integer,
            nullable=False,
            immutable=True,
            value_generation=ValueGeneration.auto_increment,
        ),
        FieldDeclaration(
            name="name",
            type=FieldType.string,
            nullable=False,
            description="The platform's display name.",
        ),
        FieldDeclaration(
            name="code",
            type=FieldType.string,
            nullable=False,
            description=(
                "Identifies the implementation class the application must use for this "
                "trading platform, such as `binance` or `metatrader_5`."
            ),
        ),
        FieldDeclaration(
            name="is_active",
            type=FieldType.boolean,
            nullable=False,
            description="Indicates whether the platform is active.",
            has_default=True,
            default=True,
        ),
        FieldDeclaration(
            name="description",
            type=FieldType.string,
            nullable=True,
            description="Describes the platform.",
        ),
    ),
    primary_key="id",
    unique_constraints=(UniqueConstraint(fields=("name",)),),
)


class TradingPlatform(Foundation, table=True):
    """Trading Platform."""

    __tablename__ = "TradingPlatform"  # pyright: ignore[reportAssignmentType]
    declaration: ClassVar[Declaration] = _DECLARATION
    __table_args__ = table_args(_DECLARATION)

    id: int | None = column(_DECLARATION, "id")
    name: str = column(_DECLARATION, "name")
    code: str = column(_DECLARATION, "code")
    is_active: bool = column(_DECLARATION, "is_active")
    description: str | None = column(_DECLARATION, "description")
