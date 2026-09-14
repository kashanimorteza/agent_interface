"""The complete Data Logic and Mapping layer: every Domain Definition's storage mapping."""

from __future__ import annotations

import model

from .accounts import AccountGroupTable, AccountTable
from .actions_positions import ActionGroupTable, ActionTable, PositionTable
from .base import Base
from .financial import AssetTable, BrokerTable, CurrencyTable
from .identity import InstanceTable, TradingPlatformTable, UserTable
from .trade_rules import (
    PartialGroupTable,
    PartialRuleTable,
    TrailingGroupTable,
    TrailingRuleTable,
)

MAPPING_REGISTRY: dict[type[model.ModelBase], type[Base]] = {
    model.User: UserTable,
    model.TradingPlatform: TradingPlatformTable,
    model.Instance: InstanceTable,
    model.Currency: CurrencyTable,
    model.Broker: BrokerTable,
    model.Asset: AssetTable,
    model.AccountGroup: AccountGroupTable,
    model.Account: AccountTable,
    model.TrailingGroup: TrailingGroupTable,
    model.TrailingRule: TrailingRuleTable,
    model.PartialGroup: PartialGroupTable,
    model.PartialRule: PartialRuleTable,
    model.ActionGroup: ActionGroupTable,
    model.Action: ActionTable,
    model.Position: PositionTable,
}

TABLE_TO_MODEL: dict[type[Base], type[model.ModelBase]] = {
    orm_cls: model_cls for model_cls, orm_cls in MAPPING_REGISTRY.items()
}

__all__ = ["MAPPING_REGISTRY", "TABLE_TO_MODEL", "Base"]
