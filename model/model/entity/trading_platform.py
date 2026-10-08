"""The Trading Platform Entity."""

from typing import ClassVar

from model.core._storage import realize_field, table_args
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    ValueGeneration,
)
from model.core.foundation import Foundation


class TradingPlatform(Foundation, table=True):
    __tablename__ = "TradingPlatform"
    declaration: ClassVar[Declaration] = Declaration(
        name="Trading Platform",
        description="Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.",
        fields=(
            FieldDeclaration(
                "id",
                FieldType.integer,
                False,
                immutable=True,
                value_generation=ValueGeneration.auto_increment,
            ),
            FieldDeclaration(
                "name",
                FieldType.string,
                False,
                description="The platform's display name.",
            ),
            FieldDeclaration(
                "code",
                FieldType.string,
                False,
                description="Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`.",
            ),
            FieldDeclaration(
                "is_active",
                FieldType.boolean,
                False,
                description="Indicates whether the platform is active.",
                default=True,
            ),
            FieldDeclaration(
                "description",
                FieldType.string,
                True,
                description="Describes the platform.",
            ),
        ),
        primary_key="id",
        unique_constraints=(("name",),),
    )
    __table_args__ = table_args(declaration)

    id: int | None = realize_field(declaration, "id")
    name: str = realize_field(declaration, "name")
    code: str = realize_field(declaration, "code")
    is_active: bool = realize_field(declaration, "is_active")
    description: str | None = realize_field(declaration, "description")
