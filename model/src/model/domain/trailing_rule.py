"""The Trailing Rule Domain Definition: one activation condition and adjustment within a Trailing Group."""

from decimal import Decimal
from typing import ClassVar

from model.foundation import DomainModel, domain_field


class TrailingRule(DomainModel):
    """A rule telling the system when and how to manage Take Profit and Stop Loss."""

    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (
        ("trailing_group_id", "trigger_percentage"),
    )

    id: int | None = domain_field(
        default=None,
        primary_key=True,
        auto_increment=True,
        nullable=False,
        description="Identifies the trailing rule.",
    )
    name: str = domain_field(
        unique=True, description="The trailing rule's display name."
    )
    trailing_group_id: int = domain_field(
        foreign_key="TrailingGroup.id",
        cardinality="many_to_one",
        description="Identifies the trailing group that contains the rule.",
    )
    trigger_percentage: Decimal = domain_field(
        description="Defines the profit percentage of the take-profit target that activates the rule."
    )
    take_profit_adjustment: Decimal | None = domain_field(
        default=None,
        description="Defines the take-profit adjustment applied when the rule is activated.",
    )
    stop_loss_adjustment: Decimal | None = domain_field(
        default=None,
        description="Defines the stop-loss adjustment applied when the rule is activated.",
    )
    is_active: bool = domain_field(
        default=True, description="Indicates whether the trailing rule is active."
    )
    description: str | None = domain_field(
        default=None, description="Describes the trailing rule."
    )
