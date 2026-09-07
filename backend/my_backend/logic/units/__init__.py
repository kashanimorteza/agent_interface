"""One Logic unit per shared Model, each defined in its own module."""

from .account import AccountLogic
from .account_group import AccountGroupLogic
from .action import ActionLogic
from .action_group import ActionGroupLogic
from .asset import AssetLogic
from .broker import BrokerLogic
from .currency import CurrencyLogic
from .partial_group import PartialGroupLogic
from .partial_rule import PartialRuleLogic
from .position import PositionLogic
from .trading_platform import TradingPlatformLogic
from .trailing_group import TrailingGroupLogic
from .trailing_rule import TrailingRuleLogic
from .user import UserLogic

UNITS = (
    UserLogic,
    CurrencyLogic,
    TradingPlatformLogic,
    BrokerLogic,
    AccountGroupLogic,
    AccountLogic,
    AssetLogic,
    TrailingGroupLogic,
    TrailingRuleLogic,
    PartialGroupLogic,
    PartialRuleLogic,
    ActionGroupLogic,
    ActionLogic,
    PositionLogic,
)

__all__ = ["UNITS", *(unit.__name__ for unit in UNITS)]
