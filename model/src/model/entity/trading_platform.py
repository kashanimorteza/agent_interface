"""The Trading Platform Entity."""

from typing import ClassVar

from sqlmodel import Field

from model.core.base import Entity
from model.core.declaration import Declaration, FieldDeclaration
from model.core.storage import column_options, table_args

_DECLARATION = Declaration(
    name="Trading Platform",
    description="Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.",
    fields=(
        FieldDeclaration(
            name="id",
            description=None,
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
    relations=(),
    unique_constraints=(("name",),),
    indexes=(),
)


class TradingPlatform(Entity, table=True):
    __table_args__ = table_args(_DECLARATION)
    declaration: ClassVar[Declaration] = _DECLARATION

    id: int | None = Field(default=None, **column_options(_DECLARATION, "id"))
    name: str = Field(
        description="The platform's display name.",
        **column_options(_DECLARATION, "name"),
    )
    code: str = Field(
        description="Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`.",
        **column_options(_DECLARATION, "code"),
    )
    is_active: bool = Field(
        default=True,
        description="Indicates whether the platform is active.",
        **column_options(_DECLARATION, "is_active"),
    )
    description: str | None = Field(
        default=None,
        description="Describes the platform.",
        **column_options(_DECLARATION, "description"),
    )
