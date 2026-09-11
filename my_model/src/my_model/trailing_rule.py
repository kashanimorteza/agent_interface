from decimal import Decimal

from pydantic import Field

from ._base import BaseModel


class TrailingRule(BaseModel):
    """An individual rule within a Trailing Group telling the system when and how to manage Take Profit and Stop Loss."""

    id: int | None = Field(
        default=None, description="Generated once the Trailing Rule is persisted."
    )
    name: str = Field(description="The trailing rule's display name.")
    trailing_group_id: int = Field(
        description="Identifies the trailing group that contains the rule."
    )
    trigger_percentage: Decimal = Field(
        description="The profit percentage of the take-profit target that activates the rule."
    )
    take_profit_adjustment: Decimal | None = Field(
        default=None,
        description="The take-profit adjustment applied when the rule is activated.",
    )
    stop_loss_adjustment: Decimal | None = Field(
        default=None,
        description="The stop-loss adjustment applied when the rule is activated.",
    )
    status: bool = Field(
        default=True, description="Indicates whether the trailing rule is active."
    )
    description: str | None = Field(
        default=None, description="Describes the trailing rule."
    )
