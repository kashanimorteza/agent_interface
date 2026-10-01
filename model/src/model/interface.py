"""The single public entrypoint of the Model: one export per Entity and the ordered collection."""

import typing as _typing

from model.core.metadata import validate_model as _validate_model
from model.entity.account import Account
from model.entity.account_group import AccountGroup
from model.entity.action import Action
from model.entity.action_group import ActionGroup
from model.entity.asset import Asset
from model.entity.broker import Broker
from model.entity.currency import Currency
from model.entity.instance import Instance
from model.entity.partial_group import PartialGroup
from model.entity.partial_rule import PartialRule
from model.entity.position import Position
from model.entity.trading_platform import TradingPlatform
from model.entity.trailing_group import TrailingGroup
from model.entity.trailing_rule import TrailingRule
from model.entity.user import User

if _typing.TYPE_CHECKING:
    from model.core.base import Entity as _Entity

entities: _typing.Final[tuple[type[_Entity], ...]] = (
    User,
    TradingPlatform,
    Instance,
    Currency,
    Broker,
    Asset,
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

_validate_model([entity.declaration for entity in entities])
