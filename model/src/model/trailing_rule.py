"""The Trailing Rule Domain Definition."""

from __future__ import annotations

from decimal import Decimal
from typing import ClassVar

from model.foundation import ModelBase, persistence_field


class TrailingRule(ModelBase):
    """One rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss.

    Provides the activation condition and the parameters used to apply the
    required adjustments.
    """

    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (
        ("trailing_group_id", "trigger_percentage"),
    )

    id: int = persistence_field(
        primary_key=True,
        auto_increment=True,
        description="Primary identity of the trailing rule.",
    )
    name: str = persistence_field(
        unique=True, description="The trailing rule's display name."
    )
    trailing_group_id: int = persistence_field(
        foreign_key="trailing_group.id",
        description="Identifies the trailing group that contains the rule.",
    )
    trigger_percentage: Decimal = persistence_field(
        description="Defines the profit percentage of the take-profit target that activates the rule."
    )
    take_profit_adjustment: Decimal | None = persistence_field(
        default=None,
        description="Defines the take-profit adjustment applied when the rule is activated.",
    )
    stop_loss_adjustment: Decimal | None = persistence_field(
        default=None,
        description="Defines the stop-loss adjustment applied when the rule is activated.",
    )
    is_active: bool = persistence_field(
        default=True, description="Indicates whether the trailing rule is active."
    )
    description: str | None = persistence_field(
        default=None, description="Describes the trailing rule."
    )
