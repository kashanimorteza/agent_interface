"""Shared logical Models of Trading Assistant.

Every Model is a validated class carrying the domain meaning that the Database,
Backend, and Frontend layers share. Each Model is exposed here exactly once under
its public symbol; consumers import only from this package root.
"""

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

__version__ = "0.1.0"

__all__ = [
    "User",
    "Currency",
    "TradingPlatform",
    "Broker",
    "AccountGroup",
    "Account",
    "Asset",
    "TrailingGroup",
    "TrailingRule",
    "PartialGroup",
    "PartialRule",
    "ActionGroup",
    "Action",
    "Position",
]
