"""The Trailing Rule Entity."""

from decimal import Decimal
from typing import ClassVar

from sqlmodel import Field

from model.core.base import Entity
from model.core.declaration import Declaration, FieldDeclaration, Relation
from model.core.storage import column_options, table_args

_DECLARATION = Declaration(
    name="Trailing Rule",
    description="Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.",
    fields=(
        FieldDeclaration(
            name="id",
            description=None,
            type="integer",
            nullable=False,
            immutable=True,
            value_generation="auto_increment",
        ),
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
        FieldDeclaration(
            name="is_active",
            description="Indicates whether the trailing rule is active.",
            type="boolean",
            nullable=False,
            has_default=True,
            default=True,
        ),
        FieldDeclaration(
            name="description",
            description="Describes the trailing rule.",
            type="string",
            nullable=True,
        ),
    ),
    primary_key="id",
    relations=(
        Relation(
            local_field="trailing_group_id",
            target_entity="Trailing Group",
            target_field="id",
        ),
    ),
    unique_constraints=(
        ("name",),
        ("trailing_group_id", "trigger_percentage"),
    ),
    indexes=(),
)


class TrailingRule(Entity, table=True):
    __table_args__ = table_args(_DECLARATION)
    declaration: ClassVar[Declaration] = _DECLARATION

    id: int | None = Field(default=None, **column_options(_DECLARATION, "id"))
    name: str = Field(
        description="The trailing rule's display name.",
        **column_options(_DECLARATION, "name"),
    )
    trailing_group_id: int = Field(
        description="Identifies the trailing group that contains the rule.",
        **column_options(_DECLARATION, "trailing_group_id"),
    )
    trigger_percentage: Decimal = Field(
        description="Defines the profit percentage of the take-profit target that activates the rule.",
        **column_options(_DECLARATION, "trigger_percentage"),
    )
    take_profit_adjustment: Decimal | None = Field(
        default=None,
        description="Defines the take-profit adjustment applied when the rule is activated.",
        **column_options(_DECLARATION, "take_profit_adjustment"),
    )
    stop_loss_adjustment: Decimal | None = Field(
        default=None,
        description="Defines the stop-loss adjustment applied when the rule is activated.",
        **column_options(_DECLARATION, "stop_loss_adjustment"),
    )
    is_active: bool = Field(
        default=True,
        description="Indicates whether the trailing rule is active.",
        **column_options(_DECLARATION, "is_active"),
    )
    description: str | None = Field(
        default=None,
        description="Describes the trailing rule.",
        **column_options(_DECLARATION, "description"),
    )
