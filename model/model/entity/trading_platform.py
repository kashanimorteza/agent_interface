"""Trading Platform Entity."""

from typing import ClassVar

from model.core import _storage as storage
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    ValueGeneration,
)
from model.core.foundation import Foundation


class TradingPlatform(Foundation, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="Trading Platform",
        description="Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.",
        primary_key="id",
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
                description="Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`.",
            ),
            FieldDeclaration(
                name="is_active",
                type=FieldType.boolean,
                nullable=False,
                description="Indicates whether the platform is active.",
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type=FieldType.string,
                nullable=True,
                description="Describes the platform.",
            ),
        ),
        unique_constraints=(("name",),),
    )
    __tablename__ = "TradingPlatform"
    __table_args__ = storage.table_args(declaration)

    id: int | None = storage.field(declaration, "id")
    name: str = storage.field(declaration, "name")
    code: str = storage.field(declaration, "code")
    is_active: bool = storage.field(declaration, "is_active")
    description: str | None = storage.field(declaration, "description")
