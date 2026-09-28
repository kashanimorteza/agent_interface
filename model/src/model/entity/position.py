"""Position Entity."""

from datetime import datetime
from decimal import Decimal

from model.declaration import Declaration
from model.entity.account import Account
from model.entity.action import Action
from model.entity.action_group import ActionGroup
from model.entity.broker import Broker
from model.entity.partial_group import PartialGroup
from model.entity.trading_platform import TradingPlatform
from model.entity.trailing_group import TrailingGroup
from model.entity.user import User
from model.foundation import Foundation


class Position(Foundation, table=True):
    """Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution."""

    id: int | None = Declaration.identity()
    user_id: int = Declaration.field(
        reference=User, description="Identifies the user who owns the position."
    )
    name: str = Declaration.field(
        unique=True, description="The position's display name."
    )
    trading_platform_id: int = Declaration.field(
        reference=TradingPlatform,
        description="Identifies the trading platform used to execute the position.",
    )
    broker_id: int = Declaration.field(
        reference=Broker,
        description="Identifies the broker through which the position is executed.",
    )
    account_id: int = Declaration.field(
        reference=Account,
        description="Identifies the trading account used for the position.",
    )
    trailing_group_id: int = Declaration.field(
        reference=TrailingGroup,
        description="Identifies the Trailing Group applied to the position.",
    )
    partial_group_id: int = Declaration.field(
        reference=PartialGroup,
        description="Identifies the Partial Group applied to the position.",
    )
    action_group_id: int = Declaration.field(
        reference=ActionGroup,
        description="Identifies the Action Group associated with the position.",
    )
    action_id: int = Declaration.field(
        reference=Action,
        description="Identifies the action from which the position is created.",
    )
    date: datetime = Declaration.field(
        description="Stores the position's date and time."
    )
    volume: Decimal = Declaration.field(
        description="Stores the position's trading volume."
    )
    profit: Decimal = Declaration.field(
        default=Decimal(0), description="Stores the position's current profit or loss."
    )
    is_executed: bool = Declaration.field(
        default=False, description="Indicates whether the position has been executed."
    )
    order_type: str = Declaration.field(description="Stores the position's order type.")
    base_tp: Decimal = Declaration.field(
        description="Stores the position's initial Take Profit value."
    )
    base_sl: Decimal = Declaration.field(
        description="Stores the position's initial Stop Loss value."
    )
    real_tp: Decimal = Declaration.field(
        description="Stores the position's current Take Profit value."
    )
    real_sl: Decimal = Declaration.field(
        description="Stores the position's current Stop Loss value."
    )
    is_active: bool = Declaration.field(
        default=True, description="Indicates whether the position is active."
    )
    description: str | None = Declaration.field(
        nullable=True, description="Describes the position."
    )
