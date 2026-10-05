from typing import ClassVar

from model.core.base import Entity
from model.core.columns import column, table_arguments
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    UniqueConstraintDeclaration,
    activity,
    identity,
)

_DECLARATION = Declaration(
    name="Trading Platform",
    description="Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.",
    fields=(
        identity(),
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
        activity("Indicates whether the platform is active."),
        FieldDeclaration(
            name="description",
            description="Describes the platform.",
            type=FieldType.STRING,
            nullable=True,
        ),
    ),
    primary_key="id",
    unique_constraints=(UniqueConstraintDeclaration(("name",)),),
)


class TradingPlatform(Entity, table=True):
    __table_args__ = table_arguments(_DECLARATION)
    declaration: ClassVar[Declaration] = _DECLARATION

    id: int | None = column(_DECLARATION, "id")
    name: str = column(_DECLARATION, "name")
    code: str = column(_DECLARATION, "code")
    is_active: bool = column(_DECLARATION, "is_active")
    description: str | None = column(_DECLARATION, "description")
