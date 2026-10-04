"""The Trailing Rule Entity."""

from decimal import Decimal

from sqlmodel import Field

from model.core._base import Entity
from model.core._defaults import (
    activity_declaration,
    activity_field,
    identity_declaration,
    identity_field,
)
from model.core._storage import DecimalText, table_arguments
from model.core.declaration import Declaration, FieldDeclaration, RelationDeclaration


class TrailingRule(Entity, table=True):
    """The Trailing Rule Entity."""

    __tablename__ = "TrailingRule"  # pyright: ignore[reportAssignmentType]
    __table_args__ = table_arguments(
        ("trailing_group_id", "trigger_percentage"),
    )

    declaration = Declaration(
        name="Trailing Rule",
        description="Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.",
        fields=(
            identity_declaration(),
            FieldDeclaration(
                name="name",
                description="The trailing rule's display name.",
                type="string",
                nullable=False,
            ),
            FieldDeclaration(
                name="trailing_group_id",
                description="Identifies the trailing group that contains the rule.",
                type="integer",
                nullable=False,
            ),
            FieldDeclaration(
                name="trigger_percentage",
                description="Defines the profit percentage of the take-profit target that activates the rule.",
                type="decimal",
                nullable=False,
            ),
            FieldDeclaration(
                name="take_profit_adjustment",
                description="Defines the take-profit adjustment applied when the rule is activated.",
                type="decimal",
                nullable=True,
            ),
            FieldDeclaration(
                name="stop_loss_adjustment",
                description="Defines the stop-loss adjustment applied when the rule is activated.",
                type="decimal",
                nullable=True,
            ),
            activity_declaration("Indicates whether the trailing rule is active."),
            FieldDeclaration(
                name="description",
                description="Describes the trailing rule.",
                type="string",
                nullable=True,
            ),
        ),
        primary_key="id",
        relations=(
            RelationDeclaration(
                local_field="trailing_group_id",
                target_entity="Trailing Group",
                target_field="id",
            ),
        ),
        unique_constraints=(("name",), ("trailing_group_id", "trigger_percentage")),
    )

    id: int | None = identity_field()
    name: str = Field(unique=True, description="The trailing rule's display name.")
    trailing_group_id: int = Field(
        foreign_key="TrailingGroup.id",
        description="Identifies the trailing group that contains the rule.",
    )
    trigger_percentage: Decimal = Field(
        sa_type=DecimalText,
        description="Defines the profit percentage of the take-profit target that activates the rule.",
    )
    take_profit_adjustment: Decimal | None = Field(
        default=None,
        sa_type=DecimalText,
        description="Defines the take-profit adjustment applied when the rule is activated.",
    )
    stop_loss_adjustment: Decimal | None = Field(
        default=None,
        sa_type=DecimalText,
        description="Defines the stop-loss adjustment applied when the rule is activated.",
    )
    is_active: bool = activity_field("Indicates whether the trailing rule is active.")
    description: str | None = Field(
        default=None, description="Describes the trailing rule."
    )
