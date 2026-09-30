"""The Trailing Rule Entity."""

from decimal import Decimal
from typing import ClassVar

from ..core.base import EntityBase
from ..core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    ValueGeneration,
)


class TrailingRule(EntityBase):
    """The Trailing Rule Entity; its Declaration states its complete meaning."""

    declaration: ClassVar[Declaration] = Declaration(
        name="Trailing Rule",
        description="Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.",
        fields=(
            FieldDeclaration(
                name="id",
                description=None,
                type=FieldType.INTEGER,
                nullable=False,
                immutable=True,
                value_generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration(
                name="name",
                description="The trailing rule's display name.",
                type=FieldType.STRING,
                nullable=False,
            ),
            FieldDeclaration(
                name="trailing_group_id",
                description="Identifies the trailing group that contains the rule.",
                type=FieldType.INTEGER,
                nullable=False,
            ),
            FieldDeclaration(
                name="trigger_percentage",
                description="Defines the profit percentage of the take-profit target that activates the rule.",
                type=FieldType.DECIMAL,
                nullable=False,
            ),
            FieldDeclaration(
                name="take_profit_adjustment",
                description="Defines the take-profit adjustment applied when the rule is activated.",
                type=FieldType.DECIMAL,
                nullable=True,
            ),
            FieldDeclaration(
                name="stop_loss_adjustment",
                description="Defines the stop-loss adjustment applied when the rule is activated.",
                type=FieldType.DECIMAL,
                nullable=True,
            ),
            FieldDeclaration(
                name="is_active",
                description="Indicates whether the trailing rule is active.",
                type=FieldType.BOOLEAN,
                nullable=False,
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                description="Describes the trailing rule.",
                type=FieldType.STRING,
                nullable=True,
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
    trigger_percentage: Decimal
    take_profit_adjustment: Decimal | None = None
    stop_loss_adjustment: Decimal | None = None
    is_active: bool = True
    description: str | None = None
