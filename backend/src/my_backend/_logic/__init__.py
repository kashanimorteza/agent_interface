from __future__ import annotations

from my_model import DomainModel

from ._base import ModelLogic
from .account import AccountLogic
from .account_group import AccountGroupLogic
from .action import ActionLogic
from .action_group import ActionGroupLogic
from .asset import AssetLogic
from .broker import BrokerLogic
from .currency import CurrencyLogic
from .instance import InstanceLogic
from .partial_group import PartialGroupLogic
from .partial_rule import PartialRuleLogic
from .position import PositionLogic
from .trading_platform import TradingPlatformLogic
from .trailing_group import TrailingGroupLogic
from .trailing_rule import TrailingRuleLogic
from .user import UserLogic

LOGIC_UNITS: dict[type[DomainModel], type[ModelLogic]] = {
    UserLogic.model_cls: UserLogic,
    TradingPlatformLogic.model_cls: TradingPlatformLogic,
    InstanceLogic.model_cls: InstanceLogic,
    CurrencyLogic.model_cls: CurrencyLogic,
    BrokerLogic.model_cls: BrokerLogic,
    AssetLogic.model_cls: AssetLogic,
    AccountGroupLogic.model_cls: AccountGroupLogic,
    AccountLogic.model_cls: AccountLogic,
    TrailingGroupLogic.model_cls: TrailingGroupLogic,
    TrailingRuleLogic.model_cls: TrailingRuleLogic,
    PartialGroupLogic.model_cls: PartialGroupLogic,
    PartialRuleLogic.model_cls: PartialRuleLogic,
    ActionGroupLogic.model_cls: ActionGroupLogic,
    ActionLogic.model_cls: ActionLogic,
    PositionLogic.model_cls: PositionLogic,
}
