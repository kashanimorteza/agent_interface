"""The Trailing Rule Domain Definition."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from .foundation import ModelBase


class TrailingRule(ModelBase):
    """An individual rule within a Trailing Group governing Take Profit and Stop Loss adjustment."""

    UNIQUE_CONSTRAINTS = (
        ("name",),
        ("trailing_group_id", "trigger_percentage"),
    )

    id: int | None = Field(default=None, description="Auto-incrementing primary key.")
    name: str = Field(..., description="The trailing rule's display name.")
    trailing_group_id: int = Field(
        ..., description="Identifies the trailing group that contains the rule."
    )
    trigger_percentage: Decimal = Field(
        ...,
        description="Defines the profit percentage of the take-profit target that "
        "activates the rule.",
    )
    take_profit_adjustment: Decimal | None = Field(
        default=None,
        description="Defines the take-profit adjustment applied when the rule is activated.",
    )
    stop_loss_adjustment: Decimal | None = Field(
        default=None,
        description="Defines the stop-loss adjustment applied when the rule is activated.",
    )
    is_active: bool = Field(default=True, description="Whether the trailing rule is active.")
    description: str | None = Field(default=None, description="Describes the trailing rule.")
