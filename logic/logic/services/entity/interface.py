"""The Entity Service Interface: the only public boundary of Entity Service."""

from database.interface import database_error, database_instance, database_value
from model import interface as _model

from logic.services.entity import account as _account
from logic.services.entity import account_group as _account_group
from logic.services.entity import action as _action
from logic.services.entity import action_group as _action_group
from logic.services.entity import asset as _asset
from logic.services.entity import broker as _broker
from logic.services.entity import currency as _currency
from logic.services.entity import instance as _instance
from logic.services.entity import partial_group as _partial_group
from logic.services.entity import partial_rule as _partial_rule
from logic.services.entity import position as _position
from logic.services.entity import trading_platform as _trading_platform
from logic.services.entity import trailing_group as _trailing_group
from logic.services.entity import trailing_rule as _trailing_rule
from logic.services.entity import user as _user


class Service:
    """Every Child Service, under the name of its Entity."""

    User = _user.User
    TradingPlatform = _trading_platform.TradingPlatform
    Instance = _instance.Instance
    Currency = _currency.Currency
    Broker = _broker.Broker
    Asset = _asset.Asset
    AccountGroup = _account_group.AccountGroup
    Account = _account.Account
    TrailingGroup = _trailing_group.TrailingGroup
    TrailingRule = _trailing_rule.TrailingRule
    PartialGroup = _partial_group.PartialGroup
    PartialRule = _partial_rule.PartialRule
    ActionGroup = _action_group.ActionGroup
    Action = _action.Action
    Position = _position.Position


class Model:
    """The Entity every Child Service binds, under the name of that Child Service."""

    User = _model.User
    TradingPlatform = _model.TradingPlatform
    Instance = _model.Instance
    Currency = _model.Currency
    Broker = _model.Broker
    Asset = _model.Asset
    AccountGroup = _model.AccountGroup
    Account = _model.Account
    TrailingGroup = _model.TrailingGroup
    TrailingRule = _model.TrailingRule
    PartialGroup = _model.PartialGroup
    PartialRule = _model.PartialRule
    ActionGroup = _model.ActionGroup
    Action = _model.Action
    Position = _model.Position


__all__ = [
    "Model",
    "Service",
    "database_error",
    "database_instance",
    "database_value",
]
