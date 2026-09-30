"""The Trading Platform Entity."""

from typing import ClassVar

from model.core.declaration import Declaration, FieldDeclaration
from model.core.foundation import Foundation


class TradingPlatform(Foundation):
    declaration: ClassVar[Declaration] = Declaration(
        name="Trading Platform",
        description="Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.",
        fields=(
            FieldDeclaration(
                name="id",
                type="integer",
                nullable=False,
                immutable=True,
                value_generation="auto_increment",
            ),
            FieldDeclaration(
                name="name",
                description="The platform's display name.",
                type="string",
                nullable=False,
            ),
            FieldDeclaration(
                name="code",
                description="Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`.",
                type="string",
                nullable=False,
            ),
            FieldDeclaration(
                name="is_active",
                description="Indicates whether the platform is active.",
                type="boolean",
                nullable=False,
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                description="Describes the platform.",
                type="string",
                nullable=True,
            ),
        ),
        primary_key="id",
        unique_constraints=(
            ("name",),
        ),
    )

    id: int | None = None
    name: str
    code: str
    is_active: bool = True
    description: str | None = None
