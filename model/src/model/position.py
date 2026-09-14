"""The Position Domain Definition."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from .foundation import ModelBase, TimezoneAwareDatetime


class Position(ModelBase):
    """The complete information for a position the system has created, executed or pending."""

    UNIQUE_CONSTRAINTS = (("name",),)

    id: int | None = Field(default=None, description="Auto-incrementing primary key.")
    user_id: int = Field(..., description="Identifies the user who owns the position.")
    name: str = Field(..., description="The position's display name.")
    trading_platform_id: int = Field(
        ..., description="Identifies the trading platform used to execute the position."
    )
    broker_id: int = Field(
        ..., description="Identifies the broker through which the position is executed."
    )
    account_id: int = Field(
        ..., description="Identifies the trading account used for the position."
    )
    trailing_group_id: int = Field(
        ..., description="Identifies the Trailing Group applied to the position."
    )
    partial_group_id: int = Field(
        ..., description="Identifies the Partial Group applied to the position."
    )
    action_group_id: int = Field(
        ..., description="Identifies the Action Group associated with the position."
    )
    action_id: int = Field(
        ..., description="Identifies the action from which the position is created."
    )
    date: TimezoneAwareDatetime = Field(..., description="Stores the position's date and time.")
    volume: Decimal = Field(..., description="Stores the position's trading volume.")
    profit: Decimal = Field(
        default=Decimal("0"), description="Stores the position's current profit or loss."
    )
    is_executed: bool = Field(default=False, description="Whether the position has been executed.")
    order_type: str = Field(..., description="Stores the position's order type.")
    base_tp: Decimal = Field(..., description="Stores the position's initial Take Profit value.")
    base_sl: Decimal = Field(..., description="Stores the position's initial Stop Loss value.")
    real_tp: Decimal = Field(..., description="Stores the position's current Take Profit value.")
    real_sl: Decimal = Field(..., description="Stores the position's current Stop Loss value.")
    is_active: bool = Field(default=True, description="Whether the position is active.")
    description: str | None = Field(default=None, description="Describes the position.")
