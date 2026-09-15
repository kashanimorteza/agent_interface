"""Model Public Interface.

Exposes every authoritative Domain Definition of the Trading Assistant
domain, together with the shared Model Foundation mechanisms, through one
explicit, stable surface.
"""

from model.account import Account
from model.account_group import AccountGroup
from model.action import Action
from model.action_group import ActionGroup
from model.asset import Asset
from model.broker import Broker
from model.currency import Currency
from model.foundation import (
    DomainModel,
    FieldContract,
    PersistenceContract,
    RelationshipContract,
)
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
    "DomainModel",
    "FieldContract",
    "Instance",
    "PartialGroup",
    "PartialRule",
    "PersistenceContract",
    "Position",
    "RelationshipContract",
    "TradingPlatform",
    "TrailingGroup",
    "TrailingRule",
    "User",
]
