"""The Partial Rule Entity."""

from decimal import Decimal
from typing import ClassVar

from model.core._storage import realize_field, table_args
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    ValueGeneration,
)
from model.core.foundation import Foundation


class PartialRule(Foundation, table=True):
    __tablename__ = "PartialRule"
    declaration: ClassVar[Declaration] = Declaration(
        name="Partial Rule",
        description="Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.",
        fields=(
            FieldDeclaration(
                "id",
                FieldType.integer,
                False,
                immutable=True,
                value_generation=ValueGeneration.auto_increment,
            ),
            FieldDeclaration(
                "name",
                FieldType.string,
                False,
                description="The partial rule's display name.",
            ),
            FieldDeclaration(
                "partial_group_id",
                FieldType.integer,
                False,
                description="Identifies the partial group that contains the rule.",
            ),
            FieldDeclaration(
                "profit_percentage",
                FieldType.decimal,
                False,
                description="Defines the profit percentage that activates the rule.",
            ),
            FieldDeclaration(
                "close_percentage",
                FieldType.decimal,
                False,
                description="Defines the percentage of the position closed when the rule is activated.",
            ),
            FieldDeclaration(
                "is_active",
                FieldType.boolean,
                False,
                description="Indicates whether the partial rule is active.",
                default=True,
            ),
            FieldDeclaration(
                "description",
                FieldType.string,
                True,
                description="Describes the partial rule.",
            ),
        ),
        primary_key="id",
        relations=(Relation("partial_group_id", "Partial Group", "id"),),
        unique_constraints=(
            ("name",),
            ("partial_group_id", "profit_percentage"),
        ),
    )
    __table_args__ = table_args(declaration)

    id: int | None = realize_field(declaration, "id")
    name: str = realize_field(declaration, "name")
    partial_group_id: int = realize_field(declaration, "partial_group_id")
    profit_percentage: Decimal = realize_field(declaration, "profit_percentage")
    close_percentage: Decimal = realize_field(declaration, "close_percentage")
    is_active: bool = realize_field(declaration, "is_active")
    description: str | None = realize_field(declaration, "description")
