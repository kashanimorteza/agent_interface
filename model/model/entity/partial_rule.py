"""The Partial Rule Entity."""

from decimal import Decimal
from typing import ClassVar

from model.core.declaration import Declaration, FieldDeclaration, Relation
from model.core.foundation import Foundation


class PartialRule(Foundation):
    declaration: ClassVar[Declaration] = Declaration(
        name="Partial Rule",
        description="Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.",
        fields=(
            FieldDeclaration(
                name="id",
                type="integer",
                nullable=False,
                immutable=True,
                value_generation="auto_increment",
            ),
            FieldDeclaration(
                name="name",
                description="The partial rule's display name.",
                type="string",
                nullable=False,
            ),
            FieldDeclaration(
                name="partial_group_id",
                description="Identifies the partial group that contains the rule.",
                type="integer",
                nullable=False,
            ),
            FieldDeclaration(
                name="profit_percentage",
                description="Defines the profit percentage that activates the rule.",
                type="decimal",
                nullable=False,
            ),
            FieldDeclaration(
                name="close_percentage",
                description="Defines the percentage of the position closed when the rule is activated.",
                type="decimal",
                nullable=False,
            ),
            FieldDeclaration(
                name="is_active",
                description="Indicates whether the partial rule is active.",
                type="boolean",
                nullable=False,
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                description="Describes the partial rule.",
                type="string",
                nullable=True,
            ),
        ),
        primary_key="id",
        relations=(
            Relation("partial_group_id", "Partial Group", "id"),
        ),
        unique_constraints=(
            ("name",),
            ("partial_group_id", "profit_percentage"),
        ),
    )

    id: int | None = None
    name: str
    partial_group_id: int
    profit_percentage: Decimal
    close_percentage: Decimal
    is_active: bool = True
    description: str | None = None
