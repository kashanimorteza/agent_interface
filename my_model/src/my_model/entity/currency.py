"""Currency Domain Entity."""

from typing import ClassVar

from sqlmodel import Field, UniqueConstraint

from my_model.model_declaration import (
    FieldDeclaration,
    LogicalType,
    ModelDeclaration,
    ReferenceDeclaration,
    ValueGeneration,
)
from my_model.model_foundation import ModelFoundation


class Currency(ModelFoundation, table=True):
    """Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision."""

    declaration: ClassVar[ModelDeclaration] = ModelDeclaration(
        entity="Currency",
        fields=(
            FieldDeclaration(
                "id", LogicalType.INTEGER, generation=ValueGeneration.AUTO_INCREMENT
            ),
            FieldDeclaration("user_id", LogicalType.INTEGER),
            FieldDeclaration("code", LogicalType.STRING, length=3),
            FieldDeclaration("symbol", LogicalType.STRING, nullable=True),
            FieldDeclaration("country", LogicalType.STRING, nullable=True),
            FieldDeclaration("decimal_digits", LogicalType.INTEGER, default=2),
            FieldDeclaration("is_active", LogicalType.BOOLEAN, default=True),
            FieldDeclaration("description", LogicalType.STRING, nullable=True),
        ),
        primary_key=("id",),
        references=(ReferenceDeclaration("user_id", "User"),),
        unique_constraints=(("user_id", "code"),),
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
