"""The project's shared domain Model package.

Publishes every resolved domain Model exactly once, together with the
credential-generation sentinel and each Model's declared initial data.
Compatible application layers import this package instead of maintaining
private copies of the same Models.
"""

from __future__ import annotations

from ._base import DomainModel
from ._generation import GENERATE_SECURELY
from .account import Account
from .account import INITIAL_DATA as ACCOUNT_INITIAL_DATA
from .account_group import AccountGroup
from .account_group import INITIAL_DATA as ACCOUNT_GROUP_INITIAL_DATA
from .action import Action
from .action import INITIAL_DATA as ACTION_INITIAL_DATA
from .action_group import ActionGroup
from .action_group import INITIAL_DATA as ACTION_GROUP_INITIAL_DATA
from .asset import Asset
from .asset import INITIAL_DATA as ASSET_INITIAL_DATA
from .broker import Broker
from .broker import INITIAL_DATA as BROKER_INITIAL_DATA
from .currency import Currency
from .currency import INITIAL_DATA as CURRENCY_INITIAL_DATA
from .instance import INITIAL_DATA as INSTANCE_INITIAL_DATA
from .instance import Instance
from .partial_group import INITIAL_DATA as PARTIAL_GROUP_INITIAL_DATA
from .partial_group import PartialGroup
from .partial_rule import PartialRule
from .position import Position
from .trading_platform import INITIAL_DATA as TRADING_PLATFORM_INITIAL_DATA
from .trading_platform import TradingPlatform
from .trailing_group import INITIAL_DATA as TRAILING_GROUP_INITIAL_DATA
from .trailing_group import TrailingGroup
from .trailing_rule import TrailingRule
from .user import INITIAL_DATA as USER_INITIAL_DATA
from .user import User

__all__ = [
    "DomainModel",
    "GENERATE_SECURELY",
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
    "INITIAL_DATA",
]

# Declared initial data for every Model that has any, keyed by the Model
# itself. Insertion and permitted credential generation are performed by
# Database; this package only declares the logical records.
INITIAL_DATA: dict[type[DomainModel], tuple[dict, ...]] = {
    User: USER_INITIAL_DATA,
    TradingPlatform: TRADING_PLATFORM_INITIAL_DATA,
    Instance: INSTANCE_INITIAL_DATA,
    Currency: CURRENCY_INITIAL_DATA,
    Broker: BROKER_INITIAL_DATA,
    Asset: ASSET_INITIAL_DATA,
    AccountGroup: ACCOUNT_GROUP_INITIAL_DATA,
    Account: ACCOUNT_INITIAL_DATA,
    TrailingGroup: TRAILING_GROUP_INITIAL_DATA,
    PartialGroup: PARTIAL_GROUP_INITIAL_DATA,
    ActionGroup: ACTION_GROUP_INITIAL_DATA,
    Action: ACTION_INITIAL_DATA,
}
