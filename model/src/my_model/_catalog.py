"""The resolved Model set and its declared initial records, in project-definition order."""

import types
from collections.abc import Mapping

from my_model._declarations import DomainModel
from my_model._initial_data import account as account_records
from my_model._initial_data import account_group as account_group_records
from my_model._initial_data import action as action_records
from my_model._initial_data import action_group as action_group_records
from my_model._initial_data import asset as asset_records
from my_model._initial_data import broker as broker_records
from my_model._initial_data import currency as currency_records
from my_model._initial_data import instance as instance_records
from my_model._initial_data import partial_group as partial_group_records
from my_model._initial_data import trading_platform as trading_platform_records
from my_model._initial_data import trailing_group as trailing_group_records
from my_model._initial_data import user as user_records
from my_model._models.account import Account
from my_model._models.account_group import AccountGroup
from my_model._models.action import Action
from my_model._models.action_group import ActionGroup
from my_model._models.asset import Asset
from my_model._models.broker import Broker
from my_model._models.currency import Currency
from my_model._models.instance import Instance
from my_model._models.partial_group import PartialGroup
from my_model._models.partial_rule import PartialRule
from my_model._models.position import Position
from my_model._models.trading_platform import TradingPlatform
from my_model._models.trailing_group import TrailingGroup
from my_model._models.trailing_rule import TrailingRule
from my_model._models.user import User

MODELS: tuple[type[DomainModel], ...] = (
    User,
    TradingPlatform,
    Currency,
    Broker,
    Asset,
    Instance,
    AccountGroup,
    Account,
    TrailingGroup,
    TrailingRule,
    PartialGroup,
    PartialRule,
    ActionGroup,
    Action,
    Position,
)
"""Every Model of the package, once each, in the order the project definition declares them."""

_INITIAL_RECORDS: Mapping[type[DomainModel], tuple[DomainModel, ...]] = types.MappingProxyType(
    {
        User: user_records.RECORDS,
        TradingPlatform: trading_platform_records.RECORDS,
        Currency: currency_records.RECORDS,
        Broker: broker_records.RECORDS,
        Asset: asset_records.RECORDS,
        Instance: instance_records.RECORDS,
        AccountGroup: account_group_records.RECORDS,
        Account: account_records.RECORDS,
        TrailingGroup: trailing_group_records.RECORDS,
        PartialGroup: partial_group_records.RECORDS,
        ActionGroup: action_group_records.RECORDS,
        Action: action_records.RECORDS,
    }
)


def initial_records[M: DomainModel](model: type[M]) -> tuple[M, ...]:
    """Return fresh copies of a Model's declared initial records, in declared order.

    A Model that declares no initial records returns an empty tuple. Changing a returned record
    never changes the declaration.
    """
    if model not in MODELS:
        raise TypeError(f"{model!r} is not a Model of this package")
    return tuple(record.model_copy(deep=True) for record in _INITIAL_RECORDS.get(model, ()))
