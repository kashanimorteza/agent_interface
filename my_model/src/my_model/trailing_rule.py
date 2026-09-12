"""The Trailing Rule domain entity: one activation rule within a Trailing Group."""

from __future__ import annotations

from decimal import Decimal
from typing import ClassVar

from pydantic import Field

from my_model._base import BaseModel


class TrailingRule(BaseModel):
    """An individual rule within a Trailing Group that tells the system when
    and how to manage Take Profit and Stop Loss.

    Provides the activation condition and the parameters used to apply the
    required adjustments.
    """

    UNIQUE_TOGETHER: ClassVar[tuple[tuple[str, ...], ...]] = (
        ("name",),
        ("trailing_group_id", "trigger_percentage"),
    )

    id: int | None = Field(
        default=None,
        description="Assigned by generation before the record is considered complete.",
    )
    name: str = Field(description="The trailing rule's display name.")
    trailing_group_id: int = Field(
        description="Identifies the trailing group that contains the rule."
    )
    trigger_percentage: Decimal = Field(
        description="Defines the profit percentage of the take-profit target that activates the rule."
    )
    take_profit_adjustment: Decimal | None = Field(
        default=None,
        description="Defines the take-profit adjustment applied when the rule is activated.",
    )
    stop_loss_adjustment: Decimal | None = Field(
        default=None,
        description="Defines the stop-loss adjustment applied when the rule is activated.",
    )
    status: bool = Field(
        default=True, description="Indicates whether the trailing rule is active."
    )
    description: str | None = Field(
        default=None, description="Describes the trailing rule."
    )
