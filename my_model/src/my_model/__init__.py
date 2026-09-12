"""my_model — the independent, platform-independent domain Model package.

Import the package namespace and address a Model type through its module:

    import my_model
    my_model.user.User(...)

or import a public module directly:

    from my_model import user
    user.User(...)

Every public entity is also re-exported at the package root as a convenience;
the module-qualified forms above remain the canonical interface.
"""

from __future__ import annotations

from . import (
    account,
    account_group,
    action,
    action_group,
    asset,
    broker,
    currency,
    instance,
    partial_group,
    partial_rule,
    position,
    trading_platform,
    trailing_group,
    trailing_rule,
    user,
)
from ._base import GENERATE_SECURELY, BaseModel
from .account import Account
from .account_group import AccountGroup
from .action import Action
from .action_group import ActionGroup
from .asset import Asset
from .broker import Broker
from .currency import Currency
from .instance import Instance
from .partial_group import PartialGroup
from .partial_rule import PartialRule
from .position import Position
from .trading_platform import TradingPlatform
from .trailing_group import TrailingGroup
from .trailing_rule import TrailingRule
from .user import User

__all__ = [
    "GENERATE_SECURELY",
    "BaseModel",
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
    "account",
    "account_group",
    "action",
    "action_group",
    "asset",
    "broker",
    "currency",
    "instance",
    "partial_group",
    "partial_rule",
    "position",
    "trading_platform",
    "trailing_group",
    "trailing_rule",
    "user",
]
