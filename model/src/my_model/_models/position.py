from datetime import datetime
from decimal import Decimal

from my_model._declarations import (
    AwaitingGeneration,
    Cardinality,
    DomainModel,
    LogicalType,
    Participation,
    Relationship,
    RelationshipKind,
    field,
)
from my_model._models.account import Account
from my_model._models.action import Action
from my_model._models.action_group import ActionGroup
from my_model._models.broker import Broker
from my_model._models.partial_group import PartialGroup
from my_model._models.trading_platform import TradingPlatform
from my_model._models.trailing_group import TrailingGroup
from my_model._models.user import User


def _uses(role: str, target: type[DomainModel], carrier: str, statement: str) -> Relationship:
    return Relationship(
        role=role,
        target=target,
        field=carrier,
        kind=RelationshipKind.USES,
        cardinality=Cardinality.MANY_TO_ONE,
        source_participation=Participation.REQUIRED,
        target_participation=Participation.OPTIONAL,
        statement=statement,
    )


class Position(DomainModel):
    """Every position the system creates, whether already executed or still pending execution."""

    logical_name = "Position"

    id: int | AwaitingGeneration = field(LogicalType.INTEGER, nullable=False, auto_increment=True, primary_key=True)
    user_id: int = field(LogicalType.INTEGER, nullable=False, purpose="Identifies the user who owns the position.")
    name: str = field(LogicalType.STRING, nullable=False, unique=True, purpose="The position's display name.")
    trading_platform_id: int = field(
        LogicalType.INTEGER, nullable=False, purpose="Identifies the trading platform used to execute the position."
    )
    broker_id: int = field(
        LogicalType.INTEGER, nullable=False, purpose="Identifies the broker through which the position is executed."
    )
    account_id: int = field(
        LogicalType.INTEGER, nullable=False, purpose="Identifies the trading account used for the position."
    )
    trailing_group_id: int = field(
        LogicalType.INTEGER, nullable=False, purpose="Identifies the Trailing Group applied to the position."
    )
    partial_group_id: int = field(
        LogicalType.INTEGER, nullable=False, purpose="Identifies the Partial Group applied to the position."
    )
    action_group_id: int = field(
        LogicalType.INTEGER, nullable=False, purpose="Identifies the Action Group associated with the position."
    )
    action_id: int = field(
        LogicalType.INTEGER, nullable=False, purpose="Identifies the action from which the position is created."
    )
    date: datetime = field(LogicalType.DATETIME, nullable=False, purpose="Stores the position's date and time.")
    volume: Decimal = field(LogicalType.DECIMAL, nullable=False, purpose="Stores the position's trading volume.")
    profit: Decimal = field(
        LogicalType.DECIMAL, nullable=False, default=Decimal("0"), purpose="Stores the position's current profit or loss."
    )
    is_executed: bool = field(
        LogicalType.BOOLEAN, nullable=False, default=False, purpose="Indicates whether the position has been executed."
    )
    order_type: str = field(LogicalType.STRING, nullable=False, purpose="Stores the position's order type.")
    base_tp: Decimal = field(
        LogicalType.DECIMAL, nullable=False, purpose="Stores the position's initial Take Profit value."
    )
    base_sl: Decimal = field(LogicalType.DECIMAL, nullable=False, purpose="Stores the position's initial Stop Loss value.")
    real_tp: Decimal = field(
        LogicalType.DECIMAL, nullable=False, purpose="Stores the position's current Take Profit value."
    )
    real_sl: Decimal = field(LogicalType.DECIMAL, nullable=False, purpose="Stores the position's current Stop Loss value.")
    status: bool = field(LogicalType.BOOLEAN, nullable=False, default=True, purpose="Indicates whether the position is active.")
    description: str | None = field(LogicalType.STRING, nullable=True, purpose="Describes the position.")

    declared_relationships = (
        Relationship(
            role="user",
            target=User,
            field="user_id",
            kind=RelationshipKind.BELONGS_TO,
            cardinality=Cardinality.MANY_TO_ONE,
            source_participation=Participation.REQUIRED,
            target_participation=Participation.OPTIONAL,
            statement="Belongs to one User through `user_id`.",
        ),
        _uses("trading platform", TradingPlatform, "trading_platform_id", "Uses one Trading Platform through `trading_platform_id`."),
        _uses("broker", Broker, "broker_id", "Uses one Broker through `broker_id`."),
        _uses("account", Account, "account_id", "Uses one Account through `account_id`."),
        _uses("trailing group", TrailingGroup, "trailing_group_id", "Uses one Trailing Group through `trailing_group_id`."),
        _uses("partial group", PartialGroup, "partial_group_id", "Uses one Partial Group through `partial_group_id`."),
        _uses("action group", ActionGroup, "action_group_id", "Uses one Action Group through `action_group_id`."),
        Relationship(
            role="action",
            target=Action,
            field="action_id",
            kind=RelationshipKind.BELONGS_TO,
            cardinality=Cardinality.MANY_TO_ONE,
            source_participation=Participation.REQUIRED,
            target_participation=Participation.OPTIONAL,
            statement="Belongs to one Action through `action_id`.",
        ),
    )
