"""The Trading Platform Entity."""

from typing import ClassVar

from sqlmodel import Field

from model.core.base import Entity
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    UniqueConstraint,
    ValueGeneration,
)


class TradingPlatform(Entity, table=True):
    """The Trading Platform Entity."""

    declaration: ClassVar[Declaration] = Declaration(
        name="Trading Platform",
        description="Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.",
        fields=(
            FieldDeclaration(
                name="id",
                type=FieldType.INTEGER,
                nullable=False,
                value_generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration(
                name="name",
                type=FieldType.STRING,
                nullable=False,
                description="The platform's display name.",
            ),
            FieldDeclaration(
                name="code",
                type=FieldType.STRING,
                nullable=False,
                description="Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`.",
            ),
            FieldDeclaration(
                name="is_active",
                type=FieldType.BOOLEAN,
                nullable=False,
                description="Indicates whether the platform is active.",
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type=FieldType.STRING,
                nullable=True,
                description="Describes the platform.",
            ),
        ),
        primary_key="id",
        unique_constraints=(UniqueConstraint(fields=("name",)),),
    )

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    code: str
    is_active: bool = True
    description: str | None = None
