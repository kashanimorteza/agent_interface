"""The Trading Platform Entity."""

from typing import ClassVar

from ..core.base import EntityBase
from ..core.declaration import Declaration, FieldDeclaration, FieldType, ValueGeneration


class TradingPlatform(EntityBase):
    """The Trading Platform Entity; its Declaration states its complete meaning."""

    declaration: ClassVar[Declaration] = Declaration(
        name="Trading Platform",
        description="Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.",
        fields=(
            FieldDeclaration(
                name="id",
                description=None,
                type=FieldType.INTEGER,
                nullable=False,
                immutable=True,
                value_generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration(
                name="name",
                description="The platform's display name.",
                type=FieldType.STRING,
                nullable=False,
            ),
            FieldDeclaration(
                name="code",
                description="Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`.",
                type=FieldType.STRING,
                nullable=False,
            ),
            FieldDeclaration(
                name="is_active",
                description="Indicates whether the platform is active.",
                type=FieldType.BOOLEAN,
                nullable=False,
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                description="Describes the platform.",
                type=FieldType.STRING,
                nullable=True,
            ),
        ),
        primary_key="id",
        unique_constraints=(("name",),),
    )

    id: int | None = None
    name: str
    code: str
    is_active: bool = True
    description: str | None = None
