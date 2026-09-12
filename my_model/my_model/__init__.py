"""Public interface of the Trading Assistant's shared, platform-independent
logical Model package.

Canonical usage::

    import my_model
    my_model.user.User(...)

Equivalent explicit usage::

    from my_model import user
    user.User(...)

Public Model types are also re-exported at the package root as a convenience;
they never replace the canonical module-qualified interface above.
"""

from my_model import (
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
from my_model._base import BaseModel
from my_model.account import Account
from my_model.account_group import AccountGroup
from my_model.action import Action
from my_model.action_group import ActionGroup
from my_model.asset import Asset
from my_model.broker import Broker
from my_model.currency import Currency
from my_model.instance import Instance
from my_model.partial_group import PartialGroup
from my_model.partial_rule import PartialRule
from my_model.position import Position
from my_model.trading_platform import TradingPlatform
from my_model.trailing_group import TrailingGroup
from my_model.trailing_rule import TrailingRule
from my_model.user import User

__all__ = [  # noqa: RUF022 (grouped by submodules then classes, not one flat sort)
    "BaseModel",
    # public submodules
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
    # package-root convenience re-exports
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
