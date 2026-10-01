"""Entity Service Interface: one Child Service per Model Entity and the types its Actions accept."""

from logic.services.entity.entity.account import AccountService
from logic.services.entity.entity.account_group import AccountGroupService
from logic.services.entity.entity.action import ActionService
from logic.services.entity.entity.action_group import ActionGroupService
from logic.services.entity.entity.asset import AssetService
from logic.services.entity.entity.broker import BrokerService
from logic.services.entity.entity.currency import CurrencyService
from logic.services.entity.entity.instance import InstanceService
from logic.services.entity.entity.partial_group import PartialGroupService
from logic.services.entity.entity.partial_rule import PartialRuleService
from logic.services.entity.entity.position import PositionService
from logic.services.entity.entity.trading_platform import TradingPlatformService
from logic.services.entity.entity.trailing_group import TrailingGroupService
from logic.services.entity.entity.trailing_rule import TrailingRuleService
from logic.services.entity.entity.user import UserService
from logic.services.entity.membership import ordered_children as _ordered_children
from logic.services.entity.naming import verify_realization as _verify_realization
from logic.services.storage.interface import (
    DatabaseInstance,
    Filter,
    FilterCombination,
    FilterOperator,
    Order,
    OrderDirection,
)

__all__ = [
    "AccountGroupService",
    "AccountService",
    "ActionGroupService",
    "ActionService",
    "AssetService",
    "BrokerService",
    "CurrencyService",
    "DatabaseInstance",
    "Filter",
    "FilterCombination",
    "FilterOperator",
    "InstanceService",
    "Order",
    "OrderDirection",
    "PartialGroupService",
    "PartialRuleService",
    "PositionService",
    "TradingPlatformService",
    "TrailingGroupService",
    "TrailingRuleService",
    "UserService",
    "children",
]

children = _ordered_children(
    [
        AccountGroupService,
        AccountService,
        ActionGroupService,
        ActionService,
        AssetService,
        BrokerService,
        CurrencyService,
        InstanceService,
        PartialGroupService,
        PartialRuleService,
        PositionService,
        TradingPlatformService,
        TrailingGroupService,
        TrailingRuleService,
        UserService,
    ]
)
_verify_realization(children)
