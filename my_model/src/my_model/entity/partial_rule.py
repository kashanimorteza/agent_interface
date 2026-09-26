"""Partial Rule Domain Entity."""

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


class PartialRule(ModelFoundation, table=True):
    """Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed."""

    declaration: ClassVar[ModelDeclaration] = ModelDeclaration(
        entity="Partial Rule",
        fields=(
            FieldDeclaration(
                "id", LogicalType.INTEGER, generation=ValueGeneration.AUTO_INCREMENT
            ),
            FieldDeclaration("name", LogicalType.STRING),
            FieldDeclaration("partial_group_id", LogicalType.INTEGER),
            FieldDeclaration("profit_percentage", LogicalType.DECIMAL),
            FieldDeclaration("close_percentage", LogicalType.DECIMAL),
            FieldDeclaration("is_active", LogicalType.BOOLEAN, default=True),
            FieldDeclaration("description", LogicalType.STRING, nullable=True),
        ),
        primary_key=("id",),
        references=(ReferenceDeclaration("partial_group_id", "Partial Group"),),
        unique_constraints=(
            ("name",),
            ("partial_group_id", "profit_percentage"),
        ),
    )

    __table_args__ = (UniqueConstraint("partial_group_id", "profit_percentage"),)

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    partial_group_id: int = Field(foreign_key="partialgroup.id")
    profit_percentage: Decimal
    close_percentage: Decimal
    is_active: bool = True
    description: str | None = None
