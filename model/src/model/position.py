"""Position Domain Definition.

The authoritative definition of the concept below. Modelling choices the Target leaves unstated are recorded here,
beside the Fields they belong to.

Recorded modelling choices:
* Text values carry no length bound: the Target states none.
* `date` is an unambiguous instant: a date and time without a timezone is rejected, and every accepted value is held in UTC without changing the instant it names.
* Volume, profit, and the base and real Take Profit and Stop Loss values are exact decimal values with no declared precision, because the Target states type `decimal` and no precision.
"""

from datetime import UTC, datetime
from decimal import Decimal
from typing import Annotated

from pydantic import AfterValidator, Field

from model.account import Account
from model.action import Action
from model.action_group import ActionGroup
from model.broker import Broker
from model.foundation import (
    ActiveFlag,
    ExactDecimal,
    GeneratedIdentity,
    ModelFoundation,
)
from model.partial_group import PartialGroup
from model.trading_platform import TradingPlatform
from model.trailing_group import TrailingGroup
from model.user import User
from model.vocabulary import Cardinality, Persistence, Reference, Unique


def _to_utc(value: datetime) -> datetime:
    """Require an unambiguous instant and normalize it to UTC without changing the instant."""
    if value.utcoffset() is None:
        raise ValueError("a date and time must state its timezone")
    return value.astimezone(UTC)


Instant = Annotated[datetime, Field(strict=False), AfterValidator(_to_utc)]
"""A timezone-aware instant held in UTC; its Plain Representation is text."""


class Position(ModelFoundation):
    """The complete information of every position the system creates, whether opened or still pending execution."""

    persistence = Persistence.PERSISTENT

    id: GeneratedIdentity = None
    user_id: Annotated[
        int,
        Reference(
            definition=User, field="id", cardinality=Cardinality.ONE, optional=False
        ),
    ]
    name: Annotated[str, Unique()]
    trading_platform_id: Annotated[
        int,
        Reference(
            definition=TradingPlatform,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
    ]
    broker_id: Annotated[
        int,
        Reference(
            definition=Broker, field="id", cardinality=Cardinality.ONE, optional=False
        ),
    ]
    account_id: Annotated[
        int,
        Reference(
            definition=Account, field="id", cardinality=Cardinality.ONE, optional=False
        ),
    ]
    trailing_group_id: Annotated[
        int,
        Reference(
            definition=TrailingGroup,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
    ]
    partial_group_id: Annotated[
        int,
        Reference(
            definition=PartialGroup,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
    ]
    action_group_id: Annotated[
        int,
        Reference(
            definition=ActionGroup,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
    ]
    action_id: Annotated[
        int,
        Reference(
            definition=Action, field="id", cardinality=Cardinality.ONE, optional=False
        ),
    ]
    date: Instant
    volume: ExactDecimal
    profit: ExactDecimal = Decimal(0)
    is_executed: bool = False
    order_type: str
    base_tp: ExactDecimal
    base_sl: ExactDecimal
    real_tp: ExactDecimal
    real_sl: ExactDecimal
    is_active: ActiveFlag = True
    description: str | None = None
