"""The Entity Service Interface: everything a caller needs to call Actions, build requests, read results and catch errors."""

from database.interface import database_error, database_instance, database_value

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
from logic.services.entity.entity.trading_platform import (
    TradingPlatform as _TradingPlatform,
)
from logic.services.entity.entity.trailing_group import TrailingGroup as _TrailingGroup
from logic.services.entity.entity.trailing_rule import TrailingRule as _TrailingRule
from logic.services.entity.entity.user import User as _User


class Service:
    """One Child Service for every Entity of the Model Entity Collection."""

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
    """The Entity every Child Service binds, under the name of its Child Service."""

    User = _User._entity
    TradingPlatform = _TradingPlatform._entity
    Instance = _Instance._entity
    Currency = _Currency._entity
    Broker = _Broker._entity
    Asset = _Asset._entity
    AccountGroup = _AccountGroup._entity
    Account = _Account._entity
    TrailingGroup = _TrailingGroup._entity
    TrailingRule = _TrailingRule._entity
    PartialGroup = _PartialGroup._entity
    PartialRule = _PartialRule._entity
    ActionGroup = _ActionGroup._entity
    Action = _Action._entity
    Position = _Position._entity


__all__ = ["Model", "Service", "database_error", "database_instance", "database_value"]
