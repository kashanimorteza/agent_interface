from decimal import Decimal
from typing import ClassVar

from sqlalchemy import Identity, UniqueConstraint
from sqlmodel import Field

from model.core._base import EntityBase
from model.core._columns import DecimalText
from model.core.declaration import Declaration, FieldDeclaration, Relation


class PartialRule(EntityBase, table=True):
    __table_args__ = (
        UniqueConstraint("partial_group_id", "profit_percentage"),
        {"sqlite_autoincrement": True},
    )
    declaration: ClassVar[Declaration] = Declaration(
        "Partial Rule",
        "Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.",
        (
            FieldDeclaration("id", None, "integer", False, immutable=True, value_generation="auto_increment"),
            FieldDeclaration("name", "The partial rule's display name.", "string", False),
            FieldDeclaration(
                "partial_group_id", "Identifies the partial group that contains the rule.", "integer", False
            ),
            FieldDeclaration(
                "profit_percentage", "Defines the profit percentage that activates the rule.", "decimal", False
            ),
            FieldDeclaration(
                "close_percentage",
                "Defines the percentage of the position closed when the rule is activated.",
                "decimal",
                False,
            ),
            FieldDeclaration(
                "is_active",
                "Indicates whether the partial rule is active.",
                "boolean",
                False,
                has_default=True,
                default=True,
            ),
            FieldDeclaration("description", "Describes the partial rule.", "string", True),
        ),
        "id",
        relations=(Relation("partial_group_id", "Partial Group", "id"),),
        unique_constraints=(
            ("name",),
            (
                "partial_group_id",
                "profit_percentage",
            ),
        ),
    )
    id: int | None = Field(default=None, primary_key=True, sa_column_args=[Identity()])
    name: str = Field(unique=True, description="The partial rule's display name.")
    partial_group_id: int = Field(
        foreign_key="PartialGroup.id", description="Identifies the partial group that contains the rule."
    )
    profit_percentage: Decimal = Field(
        sa_type=DecimalText, description="Defines the profit percentage that activates the rule."
    )
    close_percentage: Decimal = Field(
        sa_type=DecimalText, description="Defines the percentage of the position closed when the rule is activated."
    )
    is_active: bool = Field(default=True, description="Indicates whether the partial rule is active.")
    description: str | None = Field(default=None, description="Describes the partial rule.")
