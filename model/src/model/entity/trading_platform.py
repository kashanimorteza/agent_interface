"""Trading Platform Entity."""

from typing import ClassVar

from sqlmodel import Field

from model.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Generation,
    Unique,
)
from model.foundation import Foundation


class TradingPlatform(Foundation, table=True):
    """Supported trading API standard, independent of any specific exchange or broker."""

    declaration: ClassVar[Declaration] = Declaration(
        entity="TradingPlatform",
        fields=(
            FieldDeclaration(
                "id", FieldType.INTEGER, generation=Generation.AUTO_INCREMENT
            ),
            FieldDeclaration("name", FieldType.STRING),
            FieldDeclaration("code", FieldType.STRING),
            FieldDeclaration("is_active", FieldType.BOOLEAN, default=True),
            FieldDeclaration("description", FieldType.STRING, nullable=True),
        ),
        uniques=(Unique(("name",)),),
    )

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    code: str
    is_active: bool = True
    description: str | None = None
