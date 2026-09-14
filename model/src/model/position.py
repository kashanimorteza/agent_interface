"""The Position Domain Definition (Target: Model > Position)."""

from __future__ import annotations

import decimal

import pydantic

from model.foundation import (
    ExactDecimal,
    ModelFoundation,
    UTCDateTime,
    description_field,
    id_field,
    is_active_field,
)


class Position(ModelFoundation):
    """Stores the complete information for every position created by the system. It allows the
    system to identify and track positions that have been opened as well as positions that are
    still pending execution."""

    id: int = id_field()
    user_id: int = pydantic.Field(
        description="Identifies the user who owns the position."
    )
    name: str = pydantic.Field(description="The position's display name.")
    trading_platform_id: int = pydantic.Field(
        description="Identifies the trading platform used to execute the position."
    )
    broker_id: int = pydantic.Field(
        description="Identifies the broker through which the position is executed."
    )
    account_id: int = pydantic.Field(
        description="Identifies the trading account used for the position."
    )
    trailing_group_id: int = pydantic.Field(
        description="Identifies the Trailing Group applied to the position."
    )
    partial_group_id: int = pydantic.Field(
        description="Identifies the Partial Group applied to the position."
    )
    action_group_id: int = pydantic.Field(
        description="Identifies the Action Group associated with the position."
    )
    action_id: int = pydantic.Field(
        description="Identifies the action from which the position is created."
    )
    date: UTCDateTime = pydantic.Field(
        description="Stores the position's date and time."
    )
    volume: ExactDecimal = pydantic.Field(
        description="Stores the position's trading volume."
    )
    profit: ExactDecimal = pydantic.Field(
        default=decimal.Decimal(0),
        description="Stores the position's current profit or loss.",
    )
    is_executed: bool = pydantic.Field(
        default=False, description="Indicates whether the position has been executed."
    )
    order_type: str = pydantic.Field(description="Stores the position's order type.")
    base_tp: ExactDecimal = pydantic.Field(
        description="Stores the position's initial Take Profit value."
    )
    base_sl: ExactDecimal = pydantic.Field(
        description="Stores the position's initial Stop Loss value."
    )
    real_tp: ExactDecimal = pydantic.Field(
        description="Stores the position's current Take Profit value."
    )
    real_sl: ExactDecimal = pydantic.Field(
        description="Stores the position's current Stop Loss value."
    )
    is_active: bool = is_active_field("Indicates whether the position is active.")
    description: str | None = description_field("Describes the position.")
