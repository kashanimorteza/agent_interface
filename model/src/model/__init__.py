"""Model — the Trading Assistant's shared domain Model.

Public Interface: import every Domain Definition directly from ``model``.
Private internal organization (module layout, the shared Foundation) may
change without notice; only these names are supported for external use.
"""

from model.account import Account
from model.account_group import AccountGroup
from model.action import Action
from model.action_group import ActionGroup
from model.asset import Asset
from model.broker import Broker
from model.currency import Currency
from model.instance import Instance
from model.partial_group import PartialGroup
from model.partial_rule import PartialRule
from model.position import Position
from model.trading_platform import TradingPlatform
from model.trailing_group import TrailingGroup
from model.trailing_rule import TrailingRule
from model.user import User

__all__ = [
    "Account",
    "AccountGroup",
    "Action",
    "ActionGroup",
    "Asset",
    "Broker",
    "Currency",
    "Instance",
    "PartialGroup",
    "PartialRule",
    "Position",
    "TradingPlatform",
    "TrailingGroup",
    "TrailingRule",
    "User",
]
