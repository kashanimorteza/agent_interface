"""The Trading Platform Entity."""

from typing import ClassVar

from model.core._storage import realize_field, table_args
from model.core.declaration import (
    EntityDeclaration,
    FieldDeclaration,
    FieldType,
    UniqueConstraint,
    ValueGeneration,
)
from model.core.foundation import Foundation

DECLARATION = EntityDeclaration(
    name="Trading Platform",
    description="Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.",
    fields=(
        FieldDeclaration(
            "id",
            FieldType.integer,
            nullable=False,
            immutable=True,
            value_generation=ValueGeneration.auto_increment,
        ),
        FieldDeclaration(
            "name",
            FieldType.string,
            nullable=False,
            description="The platform's display name.",
        ),
        FieldDeclaration(
            "code",
            FieldType.string,
            nullable=False,
            description="Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`.",
        ),
        FieldDeclaration(
            "is_active",
            FieldType.boolean,
            nullable=False,
            description="Indicates whether the platform is active.",
            default=True,
        ),
        FieldDeclaration(
            "description",
            FieldType.string,
            nullable=True,
            description="Describes the platform.",
        ),
    ),
    unique_constraints=(UniqueConstraint(("name",)),),
)


class TradingPlatform(Foundation, table=True):
    __tablename__ = "TradingPlatform"
    __table_args__ = table_args(DECLARATION)

    declaration: ClassVar[EntityDeclaration] = DECLARATION

    id: int | None = realize_field(DECLARATION, "id")
    name: str = realize_field(DECLARATION, "name")
    code: str = realize_field(DECLARATION, "code")
    is_active: bool = realize_field(DECLARATION, "is_active")
    description: str | None = realize_field(DECLARATION, "description")
