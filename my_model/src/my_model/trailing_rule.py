"""The Trailing Rule domain entity."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from ._base import BaseModel


class TrailingRule(BaseModel):
    """An individual rule within a Trailing Group telling the system when and how
    to manage Take Profit and Stop Loss, through its activation condition and the
    adjustments it applies.
    """

    id: int | None = Field(
        default=None, description="System-generated identity, absent until persisted."
    )
    name: str = Field(min_length=1, description="The trailing rule's unique display name.")
    trailing_group_id: int = Field(
        description="Identifies the trailing group that contains the rule."
    )
    trigger_percentage: Decimal = Field(
        ge=0, description="The take-profit profit percentage that activates the rule."
    )
    take_profit_adjustment: Decimal | None = Field(
        default=None, description="Take-profit adjustment applied when the rule is activated."
    )
    stop_loss_adjustment: Decimal | None = Field(
        default=None, description="Stop-loss adjustment applied when the rule is activated."
    )
    status: bool = Field(default=True, description="Whether the trailing rule is active.")
    description: str | None = Field(default=None, description="Describes the trailing rule.")
