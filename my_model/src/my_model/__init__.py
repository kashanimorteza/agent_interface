"""Public import interface for the Trading Assistant Model package.

The canonical way to reach a domain Model is module-qualified:

    import my_model
    record = my_model.user.User(name="Ada", username="ada", password="x", api_key="y")

or equivalently:

    from my_model import user
    record = user.User(...)

Every domain submodule (and the shared `types` module) is imported here so
it is reachable as an attribute of this package without a separate import
statement. A flat class re-export (e.g. ``my_model.User``) is also provided
as a convenience, but it does not replace the module-qualified interface
above: a Model's identity is always an imported module, Model type, or
Model instance, never a string name resolved through a registry.
"""

from . import (
    account,
    account_group,
    action,
    action_group,
    asset,
    broker,
    currency,
    entity,
    instance,
    partial_group,
    partial_rule,
    position,
    trading_platform,
    trailing_group,
    trailing_rule,
    types,
    user,
)
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
    # canonical: module-qualified access (my_model.<module>.<ModelType>)
    # ("entity" is deliberately excluded: it is a domain-neutral README
    # example fixture, not part of the project's domain Model set.)
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
    "types",
    "user",
    # convenience: flat package-root re-exports
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
