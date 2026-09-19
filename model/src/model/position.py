"""Position: every position the system creates, opened or pending."""

from decimal import Decimal
from typing import Annotated

from .account import Account
from .action import Action
from .action_group import ActionGroup
from .broker import Broker
from .foundation import ExactDecimal, Flag, GeneratedId, Instant, Integer, ModelFoundation, Relationship, Text, Unique
from .partial_group import PartialGroup
from .trading_platform import TradingPlatform
from .trailing_group import TrailingGroup
from .user import User


class Position(ModelFoundation):
    persistence = "persistent"
    relationships = (
        Relationship(field="user_id", reference=User, reference_field="id", cardinality="many-to-one", optional=False),
        Relationship(field="trading_platform_id", reference=TradingPlatform, reference_field="id", cardinality="many-to-one", optional=False),
        Relationship(field="broker_id", reference=Broker, reference_field="id", cardinality="many-to-one", optional=False),
        Relationship(field="account_id", reference=Account, reference_field="id", cardinality="many-to-one", optional=False),
        Relationship(field="trailing_group_id", reference=TrailingGroup, reference_field="id", cardinality="many-to-one", optional=False),
        Relationship(field="partial_group_id", reference=PartialGroup, reference_field="id", cardinality="many-to-one", optional=False),
        Relationship(field="action_group_id", reference=ActionGroup, reference_field="id", cardinality="many-to-one", optional=False),
        Relationship(field="action_id", reference=Action, reference_field="id", cardinality="many-to-one", optional=False),
    )

    id: GeneratedId = None
    user_id: Integer
    name: Annotated[Text, Unique()]
    trading_platform_id: Integer
    broker_id: Integer
    account_id: Integer
    trailing_group_id: Integer
    partial_group_id: Integer
    action_group_id: Integer
    action_id: Integer
    # An absolute instant: timezone-aware, so a naive value is rejected.
    date: Instant
    volume: ExactDecimal
    profit: ExactDecimal = Decimal(0)
    is_executed: Flag = False
    order_type: Text
    base_tp: ExactDecimal
    base_sl: ExactDecimal
    real_tp: ExactDecimal
    real_sl: ExactDecimal
    is_active: Flag = True
    description: Text | None = None
