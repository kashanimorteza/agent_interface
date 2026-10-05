from model.entity.account import Account as Account
from model.entity.account_group import AccountGroup as AccountGroup
from model.entity.action import Action as Action
from model.entity.action_group import ActionGroup as ActionGroup
from model.entity.asset import Asset as Asset
from model.entity.broker import Broker as Broker
from model.entity.currency import Currency as Currency
from model.entity.instance import Instance as Instance
from model.entity.partial_group import PartialGroup as PartialGroup
from model.entity.partial_rule import PartialRule as PartialRule
from model.entity.position import Position as Position
from model.entity.trading_platform import TradingPlatform as TradingPlatform
from model.entity.trailing_group import TrailingGroup as TrailingGroup
from model.entity.trailing_rule import TrailingRule as TrailingRule
from model.entity.user import User as User

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
