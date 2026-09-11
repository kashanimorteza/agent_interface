from decimal import Decimal

from pydantic import AwareDatetime, Field

from ._base import BaseModel


class Position(BaseModel):
    """The complete information for every position created by the system, pending or executed."""

    id: int | None = Field(
        default=None, description="Generated once the Position is persisted."
    )
    user_id: int = Field(description="Identifies the user who owns the position.")
    name: str = Field(description="The position's display name.")
    trading_platform_id: int = Field(
        description="Identifies the trading platform used to execute the position."
    )
    broker_id: int = Field(
        description="Identifies the broker through which the position is executed."
    )
    account_id: int = Field(
        description="Identifies the trading account used for the position."
    )
    trailing_group_id: int = Field(
        description="Identifies the Trailing Group applied to the position."
    )
    partial_group_id: int = Field(
        description="Identifies the Partial Group applied to the position."
    )
    action_group_id: int = Field(
        description="Identifies the Action Group associated with the position."
    )
    action_id: int = Field(
        description="Identifies the action from which the position is created."
    )
    date: AwareDatetime = Field(description="The position's date and time.")
    volume: Decimal = Field(description="The position's trading volume.")
    profit: Decimal = Field(
        default=Decimal(0), description="The position's current profit or loss."
    )
    is_executed: bool = Field(
        default=False, description="Indicates whether the position has been executed."
    )
    order_type: str = Field(description="The position's order type.")
    base_tp: Decimal = Field(description="The position's initial Take Profit value.")
    base_sl: Decimal = Field(description="The position's initial Stop Loss value.")
    real_tp: Decimal = Field(description="The position's current Take Profit value.")
    real_sl: Decimal = Field(description="The position's current Stop Loss value.")
    status: bool = Field(
        default=True, description="Indicates whether the position is active."
    )
    description: str | None = Field(default=None, description="Describes the position.")
