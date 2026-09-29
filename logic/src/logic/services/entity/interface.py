"""Entity Service Interface: one Child Service for every Model Entity."""

from logic.services.entity.entity.user import UserService
from logic.services.entity.entity.trading_platform import TradingPlatformService
from logic.services.entity.entity.instance import InstanceService
from logic.services.entity.entity.currency import CurrencyService
from logic.services.entity.entity.broker import BrokerService
from logic.services.entity.entity.asset import AssetService
from logic.services.entity.entity.account_group import AccountGroupService
from logic.services.entity.entity.account import AccountService
from logic.services.entity.entity.trailing_group import TrailingGroupService
from logic.services.entity.entity.trailing_rule import TrailingRuleService
from logic.services.entity.entity.partial_group import PartialGroupService
from logic.services.entity.entity.partial_rule import PartialRuleService
from logic.services.entity.entity.action_group import ActionGroupService
from logic.services.entity.entity.action import ActionService
from logic.services.entity.entity.position import PositionService

__all__ = [
    "UserService",
    "TradingPlatformService",
    "InstanceService",
    "CurrencyService",
    "BrokerService",
    "AssetService",
    "AccountGroupService",
    "AccountService",
    "TrailingGroupService",
    "TrailingRuleService",
    "PartialGroupService",
    "PartialRuleService",
    "ActionGroupService",
    "ActionService",
    "PositionService",
]
