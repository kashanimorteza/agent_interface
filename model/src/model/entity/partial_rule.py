"""Partial Rule Entity."""

from decimal import Decimal
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


class PartialRule(Foundation, table=True):
    """Individual Partial Close rule stating when part of an open position closes and how much."""

    declaration: ClassVar[Declaration] = Declaration(
        entity="PartialRule",
        fields=(
            FieldDeclaration(
                "id", FieldType.INTEGER, generation=Generation.AUTO_INCREMENT
            ),
            FieldDeclaration("name", FieldType.STRING),
            FieldDeclaration("partial_group_id", FieldType.INTEGER),
            FieldDeclaration("profit_percentage", FieldType.DECIMAL),
            FieldDeclaration("close_percentage", FieldType.DECIMAL),
            FieldDeclaration("is_active", FieldType.BOOLEAN, default=True),
            FieldDeclaration("description", FieldType.STRING, nullable=True),
        ),
        references=(Reference("partial_group_id", "PartialGroup"),),
        uniques=(Unique(("name",)), Unique(("partial_group_id", "profit_percentage"))),
    )
    __table_args__ = (UniqueConstraint("partial_group_id", "profit_percentage"),)

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    partial_group_id: int = Field(foreign_key="partialgroup.id")
    profit_percentage: Decimal
    close_percentage: Decimal
    is_active: bool = True
    description: str | None = None
