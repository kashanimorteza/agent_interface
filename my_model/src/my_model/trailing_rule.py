"""The Trailing Rule domain Model: one rule within a Trailing Group."""

from decimal import Decimal

from pydantic import Field

from ._base import BaseModel
from .types import Percentage


class TrailingRule(BaseModel):
    """An individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss.

    Each rule provides the activation condition and the parameters used to
    apply the required adjustments. The combination-uniqueness of
    `trailing_group_id` and `trigger_percentage` is a domain rule traceable to
    this Model, enforced by Database.
    """

    id: int | None = Field(default=None, description="The trailing rule's generated identity.")
    name: str = Field(description="The trailing rule's display name.")
    trailing_group_id: int = Field(
        description="Identifies the trailing group that contains the rule."
    )
    trigger_percentage: Percentage = Field(
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
    description: str | None = Field(default=None, description="Describes the trailing rule.")


INITIAL_DATA: list[dict[str, object]] = []
