"""An individual rule within a Trailing Group telling the system when and how to trail Take Profit and Stop Loss."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from ._base import DomainModel


class TrailingRule(DomainModel):
    """A rule that activates at a profit trigger and adjusts Take Profit and/or Stop Loss."""

    unique_together = (("trailing_group_id", "trigger_percentage"),)

    id: int | None = Field(default=None, description="Primary key, auto-incremented.")
    name: str = Field(description="The trailing rule's display name.", json_schema_extra={"unique": True})
    trailing_group_id: int = Field(description="Identifies the trailing group that contains the rule.")
    trigger_percentage: Decimal = Field(
        description="Defines the profit percentage of the take-profit target that activates the rule."
    )
    take_profit_adjustment: Decimal | None = Field(
        default=None, description="Defines the take-profit adjustment applied when the rule is activated."
    )
    stop_loss_adjustment: Decimal | None = Field(
        default=None, description="Defines the stop-loss adjustment applied when the rule is activated."
    )
    status: bool = Field(default=True, description="Indicates whether the trailing rule is active.")
    description: str | None = Field(default=None, description="Describes the trailing rule.")
