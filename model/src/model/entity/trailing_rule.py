"""Entity: TrailingRule."""

from decimal import Decimal
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


class TrailingRule(Foundation, table=True):
    """TrailingRule Entity."""

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    trailing_group_id: int = Field(foreign_key="trailinggroup.id")
    trigger_percentage: Decimal
    take_profit_adjustment: Decimal | None = None
    stop_loss_adjustment: Decimal | None = None
    is_active: bool = True
    description: str | None = None

    __table_args__ = (UniqueConstraint("trailing_group_id", "trigger_percentage"),)

    declaration: ClassVar[Declaration] = Declaration(
        entity="TrailingRule",
        fields=(
            FieldDeclaration(
                "id", FieldType.INTEGER, value_generation=ValueGeneration.AUTO_INCREMENT
            ),
            FieldDeclaration("name", FieldType.STRING),
            FieldDeclaration("trailing_group_id", FieldType.INTEGER),
            FieldDeclaration("trigger_percentage", FieldType.DECIMAL),
            FieldDeclaration(
                "take_profit_adjustment", FieldType.DECIMAL, nullable=True
            ),
            FieldDeclaration("stop_loss_adjustment", FieldType.DECIMAL, nullable=True),
            FieldDeclaration("is_active", FieldType.BOOLEAN, default=True),
            FieldDeclaration("description", FieldType.STRING, nullable=True),
        ),
        references=(Reference("trailing_group_id", "TrailingGroup"),),
        uniques=(
            Unique(("name",)),
            Unique(
                (
                    "trailing_group_id",
                    "trigger_percentage",
                )
            ),
        ),
    )
