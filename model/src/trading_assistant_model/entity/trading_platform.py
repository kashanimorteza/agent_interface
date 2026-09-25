from typing import ClassVar

from sqlmodel import Field

from ..declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    UniqueConstraint,
    ValueGeneration,
)
from ..foundation import Foundation


class TradingPlatform(Foundation, table=True):
    """Defines a supported trading API standard, such as MetaTrader 5 or Binance, while
    keeping the system independent of any specific exchange or broker. Every trading
    platform implementation exposes the same application-facing trading functions
    through a dedicated class, while handling communication with its destination API
    according to that platform's own mechanism. Additional platform implementations can
    be added without changing the system's common trading interface.
    """

    declaration: ClassVar[Declaration] = Declaration(
        entity="TradingPlatform",
        fields=(
            FieldDeclaration(
                "id",
                FieldType.INTEGER,
                nullable=False,
                generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration("name", FieldType.STRING, nullable=False),
            FieldDeclaration("code", FieldType.STRING, nullable=False),
            FieldDeclaration(
                "is_active", FieldType.BOOLEAN, nullable=False, default=True
            ),
            FieldDeclaration("description", FieldType.STRING, nullable=True),
        ),
        primary_key=("id",),
        unique_constraints=(UniqueConstraint(("name",)),),
    )

    id: int | None = Field(
        default=None,
        primary_key=True,
        description="Unique identifier of the trading platform, assigned automatically.",
    )
    name: str = Field(description="The platform's display name.")
    code: str = Field(
        description="Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`."
    )
    is_active: bool = Field(
        default=True, description="Indicates whether the platform is active."
    )
    description: str | None = Field(default=None, description="Describes the platform.")
