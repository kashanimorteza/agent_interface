"""The Position Domain Definition.

A position created by the system, whether opened or still pending execution.

Choices where the Target is silent: declared persistent, because the Target gives the concept a
generated identity and stored records; `id` has no value until it is produced; text Fields carry
no length bound unless the Target states one; a nullable Field has no default and must be
supplied explicitly. Monetary and rate values are exact decimals. `date` is an absolute instant,
held in UTC.
"""

from decimal import Decimal
from typing import Annotated

from model.account import Account
from model.action import Action
from model.action_group import ActionGroup
from model.broker import Broker
from model.declaration import (
    Activation,
    Cardinality,
    Generated,
    Identity,
    Persistence,
    Relationship,
    Unique,
)
from model.foundation import ExactDecimal, Instant, ModelFoundation
from model.partial_group import PartialGroup
from model.trading_platform import TradingPlatform
from model.trailing_group import TrailingGroup
from model.user import User


class Position(ModelFoundation):
    persistence = Persistence.PERSISTENT
    relationships = (
        Relationship(
            name="user",
            via="user_id",
            reference=User,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
        Relationship(
            name="trading_platform",
            via="trading_platform_id",
            reference=TradingPlatform,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
        Relationship(
            name="broker",
            via="broker_id",
            reference=Broker,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
        Relationship(
            name="account",
            via="account_id",
            reference=Account,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
        Relationship(
            name="trailing_group",
            via="trailing_group_id",
            reference=TrailingGroup,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
        Relationship(
            name="partial_group",
            via="partial_group_id",
            reference=PartialGroup,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
        Relationship(
            name="action_group",
            via="action_group_id",
            reference=ActionGroup,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
        Relationship(
            name="action",
            via="action_id",
            reference=Action,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
    )

    id: Annotated[int | None, Identity(), Generated()] = None
    user_id: int
    name: Annotated[str, Unique()]
    trading_platform_id: int
    broker_id: int
    account_id: int
    trailing_group_id: int
    partial_group_id: int
    action_group_id: int
    action_id: int
    date: Instant
    volume: ExactDecimal
    profit: ExactDecimal = Decimal("0")
    is_executed: bool = False
    order_type: str
    base_tp: ExactDecimal
    base_sl: ExactDecimal
    real_tp: ExactDecimal
    real_sl: ExactDecimal
    is_active: Annotated[bool, Activation()] = True
    description: str | None
