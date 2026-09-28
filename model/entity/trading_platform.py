from typing import ClassVar

from sqlmodel import Field

from ..core.base import Entity
from ..core.declaration import Declaration, FieldDeclaration, ValueGeneration
from ..core.logical_type import LogicalType


class TradingPlatform(Entity, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="Trading Platform",
        description="Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.",
        fields=(
            FieldDeclaration(
                name="id",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=False,
                default=None,
                immutable=True,
                value_generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration(
                name="name",
                type=LogicalType.STRING,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="The platform's display name.",
            ),
            FieldDeclaration(
                name="code",
                type=LogicalType.STRING,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`.",
            ),
            FieldDeclaration(
                name="is_active",
                type=LogicalType.BOOLEAN,
                nullable=False,
                has_default=True,
                default=True,
                immutable=False,
                description="Indicates whether the platform is active.",
            ),
            FieldDeclaration(
                name="description",
                type=LogicalType.STRING,
                nullable=True,
                has_default=False,
                default=None,
                immutable=False,
                description="Describes the platform.",
            ),
        ),
        primary_key="id",
        relations=(),
        unique_constraints=(("name",),),
        indexes=(),
    )

    id: int | None = Field(default=None, primary_key=True)
    name: str
    code: str
    is_active: bool = True
    description: str | None = None
