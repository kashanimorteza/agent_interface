"""Trading Platform Entity."""

from typing import ClassVar

from ..core._storage import realize_field, table_arguments, table_name
from ..core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    UniquenessConstraint,
    ValueGeneration,
)
from ..core.foundation import Foundation

DECLARATION = Declaration(
    name="Trading Platform",
    description="Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.",
    fields=(
        FieldDeclaration(
            name="id",
            type=FieldType.integer,
            nullable=False,
            description=None,
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
    primary_key="id",
    unique_constraints=(UniquenessConstraint(fields=("name",)),),
)


class TradingPlatform(Foundation, table=True):
    __tablename__ = table_name(DECLARATION)
    __table_args__ = table_arguments(DECLARATION)

    declaration: ClassVar[Declaration] = DECLARATION

    id: int | None = realize_field(DECLARATION, "id")
    name: str = realize_field(DECLARATION, "name")
    code: str = realize_field(DECLARATION, "code")
    is_active: bool = realize_field(DECLARATION, "is_active")
    description: str | None = realize_field(DECLARATION, "description")
