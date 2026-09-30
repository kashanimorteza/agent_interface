"""The Trailing Rule Entity."""

from typing import ClassVar

from model.core._entity import Entity
from model.core._fields import activity, identity
from model.core._types import DecimalValue
from model.core.declaration import Declaration as EntityDeclaration
from model.core.declaration import FieldDeclaration, Relation


class TrailingRule(Entity):
    Declaration: ClassVar[EntityDeclaration] = EntityDeclaration(
        name="Trailing Rule",
        description=(
            "Defines an individual rule within a Trailing Group "
            "that tells the system when and how to manage Take "
            "Profit and Stop Loss. Each rule provides the "
            "activation condition and the parameters used to "
            "apply the required adjustments."
        ),
        fields=(
            identity(),
            FieldDeclaration(
                "name",
                "string",
                nullable=False,
                description="The trailing rule's display name.",
            ),
            FieldDeclaration(
                "trailing_group_id",
                "integer",
                nullable=False,
                description=("Identifies the trailing group that contains the rule."),
            ),
            FieldDeclaration(
                "trigger_percentage",
                "decimal",
                nullable=False,
                description=(
                    "Defines the profit percentage of the take-profit "
                    "target that activates the rule."
                ),
            ),
            FieldDeclaration(
                "take_profit_adjustment",
                "decimal",
                nullable=True,
                description=(
                    "Defines the take-profit adjustment applied when the "
                    "rule is activated."
                ),
            ),
            FieldDeclaration(
                "stop_loss_adjustment",
                "decimal",
                nullable=True,
                description=(
                    "Defines the stop-loss adjustment applied when the "
                    "rule is activated."
                ),
            ),
            activity("Indicates whether the trailing rule is active."),
            FieldDeclaration(
                "description",
                "string",
                nullable=True,
                description="Describes the trailing rule.",
            ),
        ),
        primary_key="id",
        relations=(Relation("trailing_group_id", "Trailing Group", "id"),),
        unique_constraints=(
            ("name",),
            ("trailing_group_id", "trigger_percentage"),
        ),
    )

    id: int | None = None
    name: str
    trailing_group_id: int
    trigger_percentage: DecimalValue
    take_profit_adjustment: DecimalValue | None = None
    stop_loss_adjustment: DecimalValue | None = None
    is_active: bool = True
    description: str | None = None
