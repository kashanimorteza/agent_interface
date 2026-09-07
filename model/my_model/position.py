"""Position: the complete information for every position created by the system."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from .account import Account
from .action import Action
from .action_group import ActionGroup
from .base import Model, Relationship, field
from .broker import Broker
from .partial_group import PartialGroup
from .trading_platform import TradingPlatform
from .trailing_group import TrailingGroup


class Position(Model):
    """Stores the complete information for every position created by the
    system. It allows the system to identify and track positions that have
    been opened as well as positions that are still pending execution."""

    id: int | None = field("integer", primary_key=True, auto_increment=True)
    name: str = field("string", unique=True, purpose="The position's display name.")
    trading_platform_id: int = field(
        "integer", purpose="Identifies the trading platform used to execute the position."
    )
    broker_id: int = field(
        "integer", purpose="Identifies the broker through which the position is executed."
    )
    account_id: int = field("integer", purpose="Identifies the trading account used for the position.")
    trailing_group_id: int = field(
        "integer", purpose="Identifies the Trailing Group applied to the position."
    )
    partial_group_id: int = field(
        "integer", purpose="Identifies the Partial Group applied to the position."
    )
    action_group_id: int = field(
        "integer", purpose="Identifies the Action Group associated with the position."
    )
    action_id: int = field(
        "integer", purpose="Identifies the action from which the position is created."
    )
    date: datetime = field("datetime", purpose="Stores the position's date and time.")
    volume: Decimal = field("decimal", purpose="Stores the position's trading volume.")
    profit: Decimal = field(
        "decimal", default=Decimal("0"), purpose="Stores the position's current profit or loss."
    )
    is_executed: bool = field(
        "boolean", default=False, purpose="Indicates whether the position has been executed."
    )
    order_type: str = field("string", purpose="Stores the position's order type.")
    base_tp: Decimal = field("decimal", purpose="Stores the position's initial Take Profit value.")
    base_sl: Decimal = field("decimal", purpose="Stores the position's initial Stop Loss value.")
    real_tp: Decimal = field("decimal", purpose="Stores the position's current Take Profit value.")
    real_sl: Decimal = field("decimal", purpose="Stores the position's current Stop Loss value.")
    status: bool = field("boolean", default=True, purpose="Indicates whether the position is active.")
    description: str | None = field("string", nullable=True, purpose="Describes the position.")

    relationships = (
        Relationship(field="trading_platform_id", target=TradingPlatform, kind="uses"),
        Relationship(field="broker_id", target=Broker, kind="uses"),
        Relationship(field="account_id", target=Account, kind="uses"),
        Relationship(field="trailing_group_id", target=TrailingGroup, kind="uses"),
        Relationship(field="partial_group_id", target=PartialGroup, kind="uses"),
        Relationship(field="action_group_id", target=ActionGroup, kind="uses"),
        Relationship(field="action_id", target=Action, kind="belongs_to"),
    )
