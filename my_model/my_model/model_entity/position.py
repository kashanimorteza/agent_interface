"""Position Domain Entity: the complete information for every position the system creates."""

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from my_model.model_declaration import Model_Declaration
from my_model.model_foundation import Model_Foundation

if TYPE_CHECKING:
    from my_model.model_entity.account import Account
    from my_model.model_entity.action import Action
    from my_model.model_entity.action_group import ActionGroup
    from my_model.model_entity.broker import Broker
    from my_model.model_entity.partial_group import PartialGroup
    from my_model.model_entity.trading_platform import TradingPlatform
    from my_model.model_entity.trailing_group import TrailingGroup
    from my_model.model_entity.user import User


class Position(Model_Declaration, Model_Foundation, table=True):
    """The complete information for a position the system has opened or still has pending."""

    __tablename__ = "position"

    user_id: int = Field(foreign_key="user.id", nullable=False)
    name: str = Field(nullable=False, unique=True)
    trading_platform_id: int = Field(foreign_key="trading_platform.id", nullable=False)
    broker_id: int = Field(foreign_key="broker.id", nullable=False)
    account_id: int = Field(foreign_key="account.id", nullable=False)
    trailing_group_id: int = Field(foreign_key="trailing_group.id", nullable=False)
    partial_group_id: int = Field(foreign_key="partial_group.id", nullable=False)
    action_group_id: int = Field(foreign_key="action_group.id", nullable=False)
    action_id: int = Field(foreign_key="action.id", nullable=False)
    date: datetime = Field(nullable=False)
    volume: Decimal = Field(nullable=False)
    profit: Decimal = Field(default=Decimal("0"), nullable=False)
    is_executed: bool = Field(default=False, nullable=False)
    order_type: str = Field(nullable=False)
    base_tp: Decimal = Field(nullable=False)
    base_sl: Decimal = Field(nullable=False)
    real_tp: Decimal = Field(nullable=False)
    real_sl: Decimal = Field(nullable=False)

    user: "User" = Relationship()
    trading_platform: "TradingPlatform" = Relationship()
    broker: "Broker" = Relationship()
    account: "Account" = Relationship()
    trailing_group: "TrailingGroup" = Relationship()
    partial_group: "PartialGroup" = Relationship()
    action_group: "ActionGroup" = Relationship()
    action: "Action" = Relationship()
