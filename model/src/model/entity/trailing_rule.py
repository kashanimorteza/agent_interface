"""Trailing Rule Entity."""

from decimal import Decimal

from model.declaration import Declaration
from model.entity.trailing_group import TrailingGroup
from model.foundation import Foundation


class TrailingRule(Foundation, table=True):
    """Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments."""

    id: int | None = Declaration.identity()
    name: str = Declaration.field(
        unique=True, description="The trailing rule's display name."
    )
    trailing_group_id: int = Declaration.field(
        reference=TrailingGroup,
        description="Identifies the trailing group that contains the rule.",
    )
    trigger_percentage: Decimal = Declaration.field(
        description="Defines the profit percentage of the take-profit target that activates the rule."
    )
    take_profit_adjustment: Decimal | None = Declaration.field(
        nullable=True,
        description="Defines the take-profit adjustment applied when the rule is activated.",
    )
    stop_loss_adjustment: Decimal | None = Declaration.field(
        nullable=True,
        description="Defines the stop-loss adjustment applied when the rule is activated.",
    )
    is_active: bool = Declaration.field(
        default=True, description="Indicates whether the trailing rule is active."
    )
    description: str | None = Declaration.field(
        nullable=True, description="Describes the trailing rule."
    )

    __table_args__ = Declaration.composite(
        "TrailingRule", unique=(("trailing_group_id", "trigger_percentage"),)
    )
