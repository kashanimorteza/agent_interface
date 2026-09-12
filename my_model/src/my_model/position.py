"""The Position domain Model: the complete information for every position the system creates."""

from datetime import datetime
from decimal import Decimal

from pydantic import Field, field_validator

from ._base import BaseModel


class Position(BaseModel):
    """Stores the complete information for every position created by the system.

    Allows the system to identify and track positions that have been opened as
    well as positions that are still pending execution. The uniqueness of
    `name` is a domain rule traceable to this Model, enforced by Database.
    """

    id: int | None = Field(default=None, description="The position's generated identity.")
    user_id: int = Field(description="Identifies the user who owns the position.")
    name: str = Field(description="The position's display name.")
    trading_platform_id: int = Field(
        description="Identifies the trading platform used to execute the position."
    )
    broker_id: int = Field(description="Identifies the broker through which the position is executed.")
    account_id: int = Field(description="Identifies the trading account used for the position.")
    trailing_group_id: int = Field(description="Identifies the Trailing Group applied to the position.")
    partial_group_id: int = Field(description="Identifies the Partial Group applied to the position.")
    action_group_id: int = Field(
        description="Identifies the Action Group associated with the position."
    )
    action_id: int = Field(description="Identifies the action from which the position is created.")
    date: datetime = Field(description="Stores the position's date and time.")
    volume: Decimal = Field(description="Stores the position's trading volume.")
    profit: Decimal = Field(default=Decimal(0), description="Stores the position's current profit or loss.")
    is_executed: bool = Field(
        default=False, description="Indicates whether the position has been executed."
    )
    order_type: str = Field(description="Stores the position's order type.")
    base_tp: Decimal = Field(description="Stores the position's initial Take Profit value.")
    base_sl: Decimal = Field(description="Stores the position's initial Stop Loss value.")
    real_tp: Decimal = Field(description="Stores the position's current Take Profit value.")
    real_sl: Decimal = Field(description="Stores the position's current Stop Loss value.")
    status: bool = Field(default=True, description="Indicates whether the position is active.")
    description: str | None = Field(default=None, description="Describes the position.")

    @field_validator("date")
    @classmethod
    def require_timezone_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("date must be timezone-aware")
        return value


INITIAL_DATA: list[dict[str, object]] = []
