"""The Position Domain Definition."""

from decimal import Decimal
from typing import Annotated

from model.entity.account import Account
from model.entity.action import Action
from model.entity.action_group import ActionGroup
from model.entity.broker import Broker
from model.entity.partial_group import PartialGroup
from model.entity.trading_platform import TradingPlatform
from model.entity.trailing_group import TrailingGroup
from model.entity.user import User
from model.foundation import (
    Declare,
    ExactDecimal,
    ModelFoundation,
    Relationship,
    UtcDatetime,
)

__all__ = ["Position"]


class Position(
    ModelFoundation,
    description="Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.",
    persistent="persistent",
    relationships=(
        Relationship(
            name="user",
            description="Belongs to one User through `user_id`.",
            definition=User,
            cardinality="1",
            optional=False,
        ),
        Relationship(
            name="trading_platform",
            description="Uses one Trading Platform through `trading_platform_id`.",
            definition=TradingPlatform,
            cardinality="1",
            optional=False,
        ),
        Relationship(
            name="broker",
            description="Uses one Broker through `broker_id`.",
            definition=Broker,
            cardinality="1",
            optional=False,
        ),
        Relationship(
            name="account",
            description="Uses one Account through `account_id`.",
            definition=Account,
            cardinality="1",
            optional=False,
        ),
        Relationship(
            name="trailing_group",
            description="Uses one Trailing Group through `trailing_group_id`.",
            definition=TrailingGroup,
            cardinality="1",
            optional=False,
        ),
        Relationship(
            name="partial_group",
            description="Uses one Partial Group through `partial_group_id`.",
            definition=PartialGroup,
            cardinality="1",
            optional=False,
        ),
        Relationship(
            name="action_group",
            description="Uses one Action Group through `action_group_id`.",
            definition=ActionGroup,
            cardinality="1",
            optional=False,
        ),
        Relationship(
            name="action",
            description="Belongs to one Action through `action_id`.",
            definition=Action,
            cardinality="1",
            optional=False,
        ),
    ),
):
    id: Annotated[
        int,
        Declare(
            description="The unique identity of the position.",
            logical_type="integer",
            identity=True,
            generated=True,
        ),
    ]
    user_id: Annotated[
        int,
        Declare(
            description="Identifies the user who owns the position.",
            logical_type="integer",
        ),
    ]
    name: Annotated[
        str,
        Declare(
            description="The position's display name.",
            logical_type="string",
            unique=True,
        ),
    ]
    trading_platform_id: Annotated[
        int,
        Declare(
            description="Identifies the trading platform used to execute the position.",
            logical_type="integer",
        ),
    ]
    broker_id: Annotated[
        int,
        Declare(
            description="Identifies the broker through which the position is executed.",
            logical_type="integer",
        ),
    ]
    account_id: Annotated[
        int,
        Declare(
            description="Identifies the trading account used for the position.",
            logical_type="integer",
        ),
    ]
    trailing_group_id: Annotated[
        int,
        Declare(
            description="Identifies the Trailing Group applied to the position.",
            logical_type="integer",
        ),
    ]
    partial_group_id: Annotated[
        int,
        Declare(
            description="Identifies the Partial Group applied to the position.",
            logical_type="integer",
        ),
    ]
    action_group_id: Annotated[
        int,
        Declare(
            description="Identifies the Action Group associated with the position.",
            logical_type="integer",
        ),
    ]
    action_id: Annotated[
        int,
        Declare(
            description="Identifies the action from which the position is created.",
            logical_type="integer",
        ),
    ]
    date: Annotated[
        UtcDatetime,
        Declare(
            description="Stores the position's date and time.", logical_type="datetime"
        ),
    ]
    volume: Annotated[
        ExactDecimal,
        Declare(
            description="Stores the position's trading volume.", logical_type="decimal"
        ),
    ]
    profit: Annotated[
        ExactDecimal,
        Declare(
            description="Stores the position's current profit or loss.",
            logical_type="decimal",
        ),
    ] = Decimal(0)
    is_executed: Annotated[
        bool,
        Declare(
            description="Indicates whether the position has been executed.",
            logical_type="boolean",
        ),
    ] = False
    order_type: Annotated[
        str,
        Declare(description="Stores the position's order type.", logical_type="string"),
    ]
    base_tp: Annotated[
        ExactDecimal,
        Declare(
            description="Stores the position's initial Take Profit value.",
            logical_type="decimal",
        ),
    ]
    base_sl: Annotated[
        ExactDecimal,
        Declare(
            description="Stores the position's initial Stop Loss value.",
            logical_type="decimal",
        ),
    ]
    real_tp: Annotated[
        ExactDecimal,
        Declare(
            description="Stores the position's current Take Profit value.",
            logical_type="decimal",
        ),
    ]
    real_sl: Annotated[
        ExactDecimal,
        Declare(
            description="Stores the position's current Stop Loss value.",
            logical_type="decimal",
        ),
    ]
    is_active: Annotated[
        bool,
        Declare(
            description="Indicates whether the position is active.",
            logical_type="boolean",
        ),
    ] = True
    description: Annotated[
        str | None,
        Declare(description="Describes the position.", logical_type="string"),
    ]
