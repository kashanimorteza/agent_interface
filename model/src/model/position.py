"""The Position Domain Definition."""

from __future__ import annotations

from decimal import Decimal

from pydantic import AwareDatetime

from model.foundation import ModelBase, persistence_field


class Position(ModelBase):
    """Stores the complete information for every position created by the system.

    Allows the system to identify and track positions that have been opened
    as well as positions that are still pending execution.
    """

    id: int = persistence_field(
        primary_key=True,
        auto_increment=True,
        description="Primary identity of the position.",
    )
    user_id: int = persistence_field(
        foreign_key="user.id", description="Identifies the user who owns the position."
    )
    name: str = persistence_field(
        unique=True, description="The position's display name."
    )
    trading_platform_id: int = persistence_field(
        foreign_key="trading_platform.id",
        description="Identifies the trading platform used to execute the position.",
    )
    broker_id: int = persistence_field(
        foreign_key="broker.id",
        description="Identifies the broker through which the position is executed.",
    )
    account_id: int = persistence_field(
        foreign_key="account.id",
        description="Identifies the trading account used for the position.",
    )
    trailing_group_id: int = persistence_field(
        foreign_key="trailing_group.id",
        description="Identifies the Trailing Group applied to the position.",
    )
    partial_group_id: int = persistence_field(
        foreign_key="partial_group.id",
        description="Identifies the Partial Group applied to the position.",
    )
    action_group_id: int = persistence_field(
        foreign_key="action_group.id",
        description="Identifies the Action Group associated with the position.",
    )
    action_id: int = persistence_field(
        foreign_key="action.id",
        description="Identifies the action from which the position is created.",
    )
    date: AwareDatetime = persistence_field(
        description="Stores the position's date and time."
    )
    volume: Decimal = persistence_field(
        description="Stores the position's trading volume."
    )
    profit: Decimal = persistence_field(
        default=Decimal(0),
        description="Stores the position's current profit or loss.",
    )
    is_executed: bool = persistence_field(
        default=False, description="Indicates whether the position has been executed."
    )
    order_type: str = persistence_field(description="Stores the position's order type.")
    base_tp: Decimal = persistence_field(
        description="Stores the position's initial Take Profit value."
    )
    base_sl: Decimal = persistence_field(
        description="Stores the position's initial Stop Loss value."
    )
    real_tp: Decimal = persistence_field(
        description="Stores the position's current Take Profit value."
    )
    real_sl: Decimal = persistence_field(
        description="Stores the position's current Stop Loss value."
    )
    is_active: bool = persistence_field(
        default=True, description="Indicates whether the position is active."
    )
    description: str | None = persistence_field(
        default=None, description="Describes the position."
    )
