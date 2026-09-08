"""The domain entities the project is made of."""

from .account import Account
from .account_group import AccountGroup
from .action import Action
from .action_group import ActionGroup
from .asset import Asset
from .broker import Broker
from .currency import Currency
from .partial_group import PartialGroup
from .partial_rule import PartialRule
from .position import Position
from .trading_platform import TradingPlatform
from .trailing_group import TrailingGroup
from .trailing_rule import TrailingRule
from .user import User

ENTITIES = (
    User,
    Currency,
    TradingPlatform,
    Broker,
    AccountGroup,
    Account,
    Asset,
    TrailingGroup,
    TrailingRule,
    PartialGroup,
    PartialRule,
    ActionGroup,
    Action,
    Position,
)

__all__ = [
    "ENTITIES",
    "Account",
    "AccountGroup",
    "Action",
    "ActionGroup",
    "Asset",
    "Broker",
    "Currency",
    "PartialGroup",
    "PartialRule",
    "Position",
    "TradingPlatform",
    "TrailingGroup",
    "TrailingRule",
    "User",
]
