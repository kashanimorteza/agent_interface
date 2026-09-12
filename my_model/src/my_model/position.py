"""The Position domain entity: the complete record of a created position."""

from __future__ import annotations

from decimal import Decimal
from typing import ClassVar

from pydantic import AwareDatetime, Field

from my_model._base import BaseModel


class Position(BaseModel):
    """Stores the complete information for every position created by the
    system.

    Allows the system to identify and track positions that have been opened
    as well as positions that are still pending execution.
    """

    UNIQUE_TOGETHER: ClassVar[tuple[tuple[str, ...], ...]] = (("name",),)

    id: int | None = Field(
        default=None,
        description="Assigned by generation before the record is considered complete.",
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
    date: AwareDatetime = Field(description="Stores the position's date and time.")
    volume: Decimal = Field(description="Stores the position's trading volume.")
    profit: Decimal = Field(
        default=Decimal(0), description="Stores the position's current profit or loss."
    )
    is_executed: bool = Field(
        default=False, description="Indicates whether the position has been executed."
    )
    order_type: str = Field(description="Stores the position's order type.")
    base_tp: Decimal = Field(
        description="Stores the position's initial Take Profit value."
    )
    base_sl: Decimal = Field(
        description="Stores the position's initial Stop Loss value."
    )
    real_tp: Decimal = Field(
        description="Stores the position's current Take Profit value."
    )
    real_sl: Decimal = Field(
        description="Stores the position's current Stop Loss value."
    )
    status: bool = Field(
        default=True, description="Indicates whether the position is active."
    )
    description: str | None = Field(default=None, description="Describes the position.")
