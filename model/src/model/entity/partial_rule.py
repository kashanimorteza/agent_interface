"""The Partial Rule Entity."""

from typing import ClassVar

from model.core._entity import Entity
from model.core._fields import activity, identity
from model.core._types import DecimalValue
from model.core.declaration import Declaration as EntityDeclaration
from model.core.declaration import FieldDeclaration, Relation


class PartialRule(Entity):
    Declaration: ClassVar[EntityDeclaration] = EntityDeclaration(
        name="Partial Rule",
        description=(
            "Defines an individual Partial Close rule that tells "
            "the system under which condition part of an open "
            "position must be closed and how much of its volume "
            "must be closed."
        ),
        fields=(
            identity(),
            FieldDeclaration(
                "name",
                "string",
                nullable=False,
                description="The partial rule's display name.",
            ),
            FieldDeclaration(
                "partial_group_id",
                "integer",
                nullable=False,
                description="Identifies the partial group that contains the rule.",
            ),
            FieldDeclaration(
                "profit_percentage",
                "decimal",
                nullable=False,
                description=("Defines the profit percentage that activates the rule."),
            ),
            FieldDeclaration(
                "close_percentage",
                "decimal",
                nullable=False,
                description=(
                    "Defines the percentage of the position closed when "
                    "the rule is activated."
                ),
            ),
            activity("Indicates whether the partial rule is active."),
            FieldDeclaration(
                "description",
                "string",
                nullable=True,
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

    id: int | None = None
    name: str
    partial_group_id: int
    profit_percentage: DecimalValue
    close_percentage: DecimalValue
    is_active: bool = True
    description: str | None = None
