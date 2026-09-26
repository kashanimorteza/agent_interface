"""Trailing Rule Domain Entity."""

from decimal import Decimal
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


class TrailingRule(ModelFoundation, table=True):
    """Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss."""

    declaration: ClassVar[ModelDeclaration] = ModelDeclaration(
        entity="Trailing Rule",
        fields=(
            FieldDeclaration(
                "id", LogicalType.INTEGER, generation=ValueGeneration.AUTO_INCREMENT
            ),
            FieldDeclaration("name", LogicalType.STRING),
            FieldDeclaration("trailing_group_id", LogicalType.INTEGER),
            FieldDeclaration("trigger_percentage", LogicalType.DECIMAL),
            FieldDeclaration(
                "take_profit_adjustment", LogicalType.DECIMAL, nullable=True
            ),
            FieldDeclaration(
                "stop_loss_adjustment", LogicalType.DECIMAL, nullable=True
            ),
            FieldDeclaration("is_active", LogicalType.BOOLEAN, default=True),
            FieldDeclaration("description", LogicalType.STRING, nullable=True),
        ),
        primary_key=("id",),
        references=(ReferenceDeclaration("trailing_group_id", "Trailing Group"),),
        unique_constraints=(
            ("name",),
            ("trailing_group_id", "trigger_percentage"),
        ),
    )

    __table_args__ = (UniqueConstraint("trailing_group_id", "trigger_percentage"),)

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    trailing_group_id: int = Field(foreign_key="trailinggroup.id")
    trigger_percentage: Decimal
    take_profit_adjustment: Decimal | None = None
    stop_loss_adjustment: Decimal | None = None
    is_active: bool = True
    description: str | None = None
