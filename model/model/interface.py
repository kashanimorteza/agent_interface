"""Interface: the package-root entrypoint through which every Entity is published."""

from model.core._storage import check_relations
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

#: Every Entity once, in Target order.
entities = (
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

check_relations(tuple(entity.declaration for entity in entities))
