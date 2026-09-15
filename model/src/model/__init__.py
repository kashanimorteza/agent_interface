"""Public Interface of the Model Component.

Exposes every authoritative Domain Definition defined for this Target through
one stable, explicit surface.
"""

from model.account import Account
from model.account_group import AccountGroup
from model.action import Action
from model.action_group import ActionGroup
from model.asset import Asset
from model.broker import Broker
from model.currency import Currency
from model.foundation import Credential, DomainModel, ForeignKey
from model.instance import Instance
from model.partial_group import PartialGroup
from model.partial_rule import PartialRule
from model.position import Position
from model.trading_platform import TradingPlatform
from model.trailing_group import TrailingGroup
from model.trailing_rule import TrailingRule
from model.user import User

__all__ = [
    "Credential",
    "DomainModel",
    "ForeignKey",
    "User",
    "TradingPlatform",
    "Instance",
    "Currency",
    "Broker",
    "Asset",
    "AccountGroup",
    "Account",
    "TrailingGroup",
    "TrailingRule",
    "PartialGroup",
    "PartialRule",
    "ActionGroup",
    "Action",
    "Position",
]
