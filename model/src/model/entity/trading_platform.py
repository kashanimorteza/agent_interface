"""Entity: TradingPlatform."""

from typing import ClassVar

from sqlmodel import Field

from model.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Unique,
    ValueGeneration,
)
from model.foundation import Foundation


class TradingPlatform(Foundation, table=True):
    """TradingPlatform Entity."""

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    code: str
    is_active: bool = True
    description: str | None = None

    declaration: ClassVar[Declaration] = Declaration(
        entity="TradingPlatform",
        fields=(
            FieldDeclaration(
                "id", FieldType.INTEGER, value_generation=ValueGeneration.AUTO_INCREMENT
            ),
            FieldDeclaration("name", FieldType.STRING),
            FieldDeclaration("code", FieldType.STRING),
            FieldDeclaration("is_active", FieldType.BOOLEAN, default=True),
            FieldDeclaration("description", FieldType.STRING, nullable=True),
        ),
        uniques=(Unique(("name",)),),
    )
