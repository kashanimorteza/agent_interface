from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import ClassVar

from pydantic import Field

from ._base import DomainModel
from ._shared import Relationship


class Position(DomainModel):
    user_id: int = Field(..., description="Identifies the user who owns the position.")
    name: str = Field(..., description="The position's display name.")
    trading_platform_id: int = Field(
        ..., description="Identifies the trading platform used to execute the position."
    )
    broker_id: int = Field(..., description="Identifies the broker through which the position is executed.")
    account_id: int = Field(..., description="Identifies the trading account used for the position.")
    trailing_group_id: int = Field(..., description="Identifies the Trailing Group applied to the position.")
    partial_group_id: int = Field(..., description="Identifies the Partial Group applied to the position.")
    action_group_id: int = Field(
        ..., description="Identifies the Action Group associated with the position."
    )
    action_id: int = Field(..., description="Identifies the action from which the position is created.")
    date: datetime = Field(..., description="Stores the position's date and time.")
    volume: Decimal = Field(..., description="Stores the position's trading volume.")
    profit: Decimal = Field(default=Decimal("0"), description="Stores the position's current profit or loss.")
    is_executed: bool = Field(default=False, description="Indicates whether the position has been executed.")
    order_type: str = Field(..., description="Stores the position's order type.")
    base_tp: Decimal = Field(..., description="Stores the position's initial Take Profit value.")
    base_sl: Decimal = Field(..., description="Stores the position's initial Stop Loss value.")
    real_tp: Decimal = Field(..., description="Stores the position's current Take Profit value.")
    real_sl: Decimal = Field(..., description="Stores the position's current Stop Loss value.")
    status: bool = Field(default=True, description="Indicates whether the position is active.")
    description: str | None = Field(default=None, description="Describes the position.")

    unique_fields: ClassVar[frozenset[str]] = frozenset({"name"})
    relationships: ClassVar[dict[str, Relationship]] = {
        "user": Relationship(target="User", cardinality="one", field="user_id"),
        "trading_platform": Relationship(
            target="TradingPlatform", cardinality="one", field="trading_platform_id"
        ),
        "broker": Relationship(target="Broker", cardinality="one", field="broker_id"),
        "account": Relationship(target="Account", cardinality="one", field="account_id"),
        "trailing_group": Relationship(
            target="TrailingGroup", cardinality="one", field="trailing_group_id"
        ),
        "partial_group": Relationship(target="PartialGroup", cardinality="one", field="partial_group_id"),
        "action_group": Relationship(target="ActionGroup", cardinality="one", field="action_group_id"),
        "action": Relationship(target="Action", cardinality="one", field="action_id"),
    }
