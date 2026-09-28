"""Currency Entity."""

from typing import ClassVar

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from model.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Generation,
    Reference,
    Unique,
)
from model.foundation import Foundation


class Currency(Foundation, table=True):
    """Currency usable by the trading system, with its standard code, symbol, region, and decimal precision."""

    declaration: ClassVar[Declaration] = Declaration(
        entity="Currency",
        fields=(
            FieldDeclaration(
                "id", FieldType.INTEGER, generation=Generation.AUTO_INCREMENT
            ),
            FieldDeclaration("user_id", FieldType.INTEGER),
            FieldDeclaration("code", FieldType.STRING, length=3),
            FieldDeclaration("symbol", FieldType.STRING, nullable=True),
            FieldDeclaration("country", FieldType.STRING, nullable=True),
            FieldDeclaration("decimal_digits", FieldType.INTEGER, default=2),
            FieldDeclaration("is_active", FieldType.BOOLEAN, default=True),
            FieldDeclaration("description", FieldType.STRING, nullable=True),
        ),
        references=(Reference("user_id", "User"),),
        uniques=(Unique(("user_id", "code")),),
    )
    __table_args__ = (UniqueConstraint("user_id", "code"),)

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    code: str = Field(max_length=3)
    symbol: str | None = None
    country: str | None = None
    decimal_digits: int = 2
    is_active: bool = True
    description: str | None = None
