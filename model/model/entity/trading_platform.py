"""The Trading Platform Entity."""

from typing import ClassVar

from model.core._storage import mapped_field, table_arguments
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    UniquenessConstraint,
    ValueGeneration,
)
from model.core.foundation import Foundation


class TradingPlatform(Foundation, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="Trading Platform",
        description=(
            "Defines a supported trading API standard, such as MetaTrader 5 or Binance, while "
            "keeping the system independent of any specific exchange or broker. Every trading "
            "platform implementation exposes the same application-facing trading functions "
            "through a dedicated class, while handling communication with its destination API "
            "according to that platform's own mechanism. Additional platform implementations "
            "can be added without changing the system's common trading interface."
        ),
        fields=(
            FieldDeclaration(
                name="id",
                type=FieldType.INTEGER,
                nullable=False,
                immutable=True,
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
                description=(
                    "Identifies the implementation class the application must use for this "
                    "trading platform, such as `binance` or `metatrader_5`."
                ),
            ),
            FieldDeclaration(
                name="is_active",
                type=FieldType.BOOLEAN,
                nullable=False,
                description="Indicates whether the platform is active.",
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type=FieldType.STRING,
                nullable=True,
                description="Describes the platform.",
            ),
        ),
        unique_constraints=(UniquenessConstraint(("name",)),),
    )

    __tablename__ = "TradingPlatform"
    __table_args__ = table_arguments(declaration)

    id: int | None = mapped_field(declaration, "id")
    name: str = mapped_field(declaration, "name")
    code: str = mapped_field(declaration, "code")
    is_active: bool = mapped_field(declaration, "is_active")
    description: str | None = mapped_field(declaration, "description")
