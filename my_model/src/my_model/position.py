"""The Position domain entity."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import Field

from ._base import BaseModel


class Position(BaseModel):
    """The complete information for a position created by the system, whether
    already opened or still pending execution.
    """

    id: int | None = Field(
        default=None, description="System-generated identity, absent until persisted."
    )
    user_id: int = Field(description="Identifies the user who owns the position.")
    name: str = Field(min_length=1, description="The position's unique display name.")
    trading_platform_id: int = Field(
        description="Identifies the trading platform used to execute the position."
    )
    broker_id: int = Field(
        description="Identifies the broker through which the position is executed."
    )
    account_id: int = Field(description="Identifies the trading account used for the position.")
    trailing_group_id: int = Field(
        description="Identifies the Trailing Group applied to the position."
    )
    partial_group_id: int = Field(
        description="Identifies the Partial Group applied to the position."
    )
    action_group_id: int = Field(
        description="Identifies the Action Group associated with the position."
    )
    action_id: int = Field(description="Identifies the action from which the position is created.")
    date: datetime = Field(description="The position's date and time.")
    volume: Decimal = Field(gt=0, description="The position's trading volume.")
    profit: Decimal = Field(
        default=Decimal("0"), description="The position's current profit or loss."
    )
    is_executed: bool = Field(default=False, description="Whether the position has been executed.")
    order_type: str = Field(min_length=1, description="The position's order type.")
    base_tp: Decimal = Field(description="The position's initial Take Profit value.")
    base_sl: Decimal = Field(description="The position's initial Stop Loss value.")
    real_tp: Decimal = Field(description="The position's current Take Profit value.")
    real_sl: Decimal = Field(description="The position's current Stop Loss value.")
    status: bool = Field(default=True, description="Whether the position is active.")
    description: str | None = Field(default=None, description="Describes the position.")
