"""Trading Platform Entity."""

from typing import ClassVar

from sqlmodel import Field

from my_model.model_declaration import (
    FieldDeclaration,
    LogicalType,
    ModelDeclaration,
    UniquenessConstraint,
    ValueGeneration,
)
from my_model.model_foundation import ModelFoundation


class TradingPlatform(ModelFoundation, table=True):
    """Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker."""

    declaration: ClassVar[ModelDeclaration] = ModelDeclaration(
        entity="TradingPlatform",
        purpose="Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.",
        fields=(
            FieldDeclaration(
                "id",
                LogicalType.INTEGER,
                generation=ValueGeneration.AUTO_INCREMENT,
                purpose="",
            ),
            FieldDeclaration(
                "name", LogicalType.STRING, purpose="The platform's display name"
            ),
            FieldDeclaration(
                "code",
                LogicalType.STRING,
                purpose="Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`",
            ),
            FieldDeclaration(
                "is_active",
                LogicalType.BOOLEAN,
                has_default=True,
                default=True,
                purpose="Indicates whether the platform is active",
            ),
            FieldDeclaration(
                "description",
                LogicalType.STRING,
                nullable=True,
                purpose="Describes the platform",
            ),
        ),
        unique_constraints=(UniquenessConstraint(("name",)),),
    )

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    code: str
    is_active: bool = True
    description: str | None = None
