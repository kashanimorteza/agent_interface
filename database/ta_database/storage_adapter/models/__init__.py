"""Table mappings of the Storage Adapter, one per resolved table.

Importing this package registers every table on ``Base.metadata`` and exposes
``MODEL_REGISTRY``, which resolves a Model key (exactly as indexed in the
shared Model configuration) to its mapped class.
"""

from __future__ import annotations

from ta_database.storage_adapter.base import Base
from ta_database.storage_adapter.models.account import Account
from ta_database.storage_adapter.models.action import Action
from ta_database.storage_adapter.models.action_group import ActionGroup
from ta_database.storage_adapter.models.asset import Asset
from ta_database.storage_adapter.models.broker import Broker
from ta_database.storage_adapter.models.currency import Currency
from ta_database.storage_adapter.models.partial_group import PartialGroup
from ta_database.storage_adapter.models.partial_rule import PartialRule
from ta_database.storage_adapter.models.position import Position
from ta_database.storage_adapter.models.trading_platform import TradingPlatform
from ta_database.storage_adapter.models.trailing_group import TrailingGroup
from ta_database.storage_adapter.models.trailing_rule import TrailingRule
from ta_database.storage_adapter.models.user import User

MODEL_REGISTRY: dict[str, type[Base]] = {
    "user": User,
    "currency": Currency,
    "trading_platform": TradingPlatform,
    "broker": Broker,
    "account": Account,
    "asset": Asset,
    "trailing_group": TrailingGroup,
    "trailing_rule": TrailingRule,
    "partial_group": PartialGroup,
    "partial_rule": PartialRule,
    "action_group": ActionGroup,
    "action": Action,
    "position": Position,
}

__all__ = ["Base", "MODEL_REGISTRY", *[cls.__name__ for cls in MODEL_REGISTRY.values()]]
