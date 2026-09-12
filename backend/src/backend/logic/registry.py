"""Connects every Model's separately defined Logic unit. Defines none itself."""

from __future__ import annotations

import my_model as m

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

REGISTRY: dict[type[m.BaseModel], ModelLogic] = {
    m.User: UserLogic(),
    m.TradingPlatform: TradingPlatformLogic(),
    m.Instance: InstanceLogic(),
    m.Currency: CurrencyLogic(),
    m.Broker: BrokerLogic(),
    m.Asset: AssetLogic(),
    m.AccountGroup: AccountGroupLogic(),
    m.Account: AccountLogic(),
    m.TrailingGroup: TrailingGroupLogic(),
    m.TrailingRule: TrailingRuleLogic(),
    m.PartialGroup: PartialGroupLogic(),
    m.PartialRule: PartialRuleLogic(),
    m.ActionGroup: ActionGroupLogic(),
    m.Action: ActionLogic(),
    m.Position: PositionLogic(),
}
