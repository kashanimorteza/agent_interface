"""Model's Public Interface (Model Principle 5): the shared domain Model of the Trading Assistant.

Every authoritative Domain Definition is exported at package level, `model.<DomainDefinition>`,
as the one unambiguous public identity for each. Consumers use this surface rather than a
Domain Definition's private module path.
"""

from __future__ import annotations

from model.account import Account
from model.account_group import AccountGroup
from model.action import Action
from model.action_group import ActionGroup
from model.asset import Asset
from model.broker import Broker
from model.currency import Currency
from model.foundation import (
    DEFAULT_MODEL_OPERATIONS,
    ExactDecimal,
    ModelFoundation,
    UTCDateTime,
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
    "DEFAULT_MODEL_OPERATIONS",
    "Account",
    "AccountGroup",
    "Action",
    "ActionGroup",
    "Asset",
    "Broker",
    "Currency",
    "ExactDecimal",
    "Instance",
    "ModelFoundation",
    "PartialGroup",
    "PartialRule",
    "Position",
    "TradingPlatform",
    "TrailingGroup",
    "TrailingRule",
    "UTCDateTime",
    "User",
]
