"""Registers every Model Logic unit, keyed by its Domain Definition, for the API layer."""

from __future__ import annotations

from ..model_interface import ModelBase
from .account import AccountLogic
from .account_group import AccountGroupLogic
from .action import ActionLogic
from .action_group import ActionGroupLogic
from .asset import AssetLogic
from .broker import BrokerLogic
from .currency import CurrencyLogic
from .foundation import ModelLogicBase
from .instance import InstanceLogic
from .partial_group import PartialGroupLogic
from .partial_rule import PartialRuleLogic
from .position import PositionLogic
from .trading_platform import TradingPlatformLogic
from .trailing_group import TrailingGroupLogic
from .trailing_rule import TrailingRuleLogic
from .user import UserLogic

LOGIC_REGISTRY: tuple[type[ModelLogicBase[ModelBase]], ...] = (
    UserLogic,
    TradingPlatformLogic,
    InstanceLogic,
    CurrencyLogic,
    BrokerLogic,
    AssetLogic,
    AccountGroupLogic,
    AccountLogic,
    TrailingGroupLogic,
    TrailingRuleLogic,
    PartialGroupLogic,
    PartialRuleLogic,
    ActionGroupLogic,
    ActionLogic,
    PositionLogic,
)
"""Every Model Logic unit, in the same dependency order as their Domain Definitions."""

__all__ = ["LOGIC_REGISTRY", "ModelLogicBase"]
