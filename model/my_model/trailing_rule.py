"""Trailing Rule: one rule within a Trailing Group."""

from __future__ import annotations

from decimal import Decimal

from .base import Model, Relationship, field
from .trailing_group import TrailingGroup


class TrailingRule(Model):
    """Defines an individual rule within a Trailing Group that tells the
    system when and how to manage Take Profit and Stop Loss. Each rule
    provides the activation condition and the parameters used to apply the
    required adjustments."""

    logical_name = "Trailing Rule"

    id: int | None = field("integer", primary_key=True, auto_increment=True)
    name: str = field("string", unique=True, purpose="The trailing rule's display name.")
    trailing_group_id: int = field(
        "integer", purpose="Identifies the trailing group that contains the rule."
    )
    trigger_percentage: Decimal = field(
        "decimal",
        purpose="Defines the profit percentage of the take-profit target that activates the rule.",
    )
    take_profit_adjustment: Decimal | None = field(
        "decimal",
        nullable=True,
        purpose="Defines the take-profit adjustment applied when the rule is activated.",
    )
    stop_loss_adjustment: Decimal | None = field(
        "decimal",
        nullable=True,
        purpose="Defines the stop-loss adjustment applied when the rule is activated.",
    )
    status: bool = field("boolean", default=True, purpose="Indicates whether the trailing rule is active.")
    description: str | None = field("string", nullable=True, purpose="Describes the trailing rule.")

    relationships = (
        Relationship(field="trailing_group_id", target=TrailingGroup, kind="belongs_to"),
    )
