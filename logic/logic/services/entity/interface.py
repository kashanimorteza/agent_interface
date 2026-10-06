"""The Entity Service Interface: Child Services, bound Entities, and Storage contracts."""

from model import interface as _model

from logic.services.entity.entity.account import Account as _Account
from logic.services.entity.entity.account_group import AccountGroup as _AccountGroup
from logic.services.entity.entity.action import Action as _Action
from logic.services.entity.entity.action_group import ActionGroup as _ActionGroup
from logic.services.entity.entity.asset import Asset as _Asset
from logic.services.entity.entity.broker import Broker as _Broker
from logic.services.entity.entity.currency import Currency as _Currency
from logic.services.entity.entity.instance import Instance as _Instance
from logic.services.entity.entity.partial_group import PartialGroup as _PartialGroup
from logic.services.entity.entity.partial_rule import PartialRule as _PartialRule
from logic.services.entity.entity.position import Position as _Position
from logic.services.entity.entity.trading_platform import TradingPlatform as _TradingPlatform
from logic.services.entity.entity.trailing_group import TrailingGroup as _TrailingGroup
from logic.services.entity.entity.trailing_rule import TrailingRule as _TrailingRule
from logic.services.entity.entity.user import User as _User
from logic.services.storage import interface as _storage


class Service:
    """Every Child Service, one for every Entity."""

    User = _User
    TradingPlatform = _TradingPlatform
    Instance = _Instance
    Currency = _Currency
    Broker = _Broker
    Asset = _Asset
    AccountGroup = _AccountGroup
    Account = _Account
    TrailingGroup = _TrailingGroup
    TrailingRule = _TrailingRule
    PartialGroup = _PartialGroup
    PartialRule = _PartialRule
    ActionGroup = _ActionGroup
    Action = _Action
    Position = _Position


class Model:
    """The Entity each Child Service binds, under the Child Service name."""

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


class Parameter:
    """Every Storage contract that is not an error, except the gateway."""

    CommandResult = _storage.CommandResult
    DatabaseInstance = _storage.DatabaseInstance
    Filter = _storage.Filter
    FilterCombination = _storage.FilterCombination
    FilterOperator = _storage.FilterOperator
    LifecycleResult = _storage.LifecycleResult
    Order = _storage.Order
    OrderDirection = _storage.OrderDirection


class Error:
    """Every error Storage publishes."""

    ConfigurationError = _storage.ConfigurationError
    ConnectionFailureError = _storage.ConnectionFailureError
    DatabaseError = _storage.DatabaseError
    DeclarationMismatchError = _storage.DeclarationMismatchError
    ExecutionError = _storage.ExecutionError
    InactiveInstanceError = _storage.InactiveInstanceError
    InvalidInputError = _storage.InvalidInputError
    LifecycleError = _storage.LifecycleError


__all__ = ["Service", "Model", "Parameter", "Error"]
