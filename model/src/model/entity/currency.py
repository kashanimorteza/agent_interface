"""Entity: Currency."""

from typing import ClassVar

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from model.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Reference,
    Unique,
    ValueGeneration,
)
from model.foundation import Foundation


class Currency(Foundation, table=True):
    """Currency Entity."""

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    code: str = Field(max_length=3)
    symbol: str | None = None
    country: str | None = None
    decimal_digits: int = 2
    is_active: bool = True
    description: str | None = None

    __table_args__ = (UniqueConstraint("user_id", "code"),)

    declaration: ClassVar[Declaration] = Declaration(
        entity="Currency",
        fields=(
            FieldDeclaration(
                "id", FieldType.INTEGER, value_generation=ValueGeneration.AUTO_INCREMENT
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
        uniques=(
            Unique(
                (
                    "user_id",
                    "code",
                )
            ),
        ),
    )
