"""The Account Domain Definition."""

from decimal import Decimal
from typing import Annotated

from model.entity.account_group import AccountGroup
from model.entity.broker import Broker
from model.entity.currency import Currency
from model.entity.instance import Instance
from model.foundation import (
    Constraint,
    Declare,
    ExactDecimal,
    ModelFoundation,
    Relationship,
    Sensitivity,
)

__all__ = ["Account"]


class Account(
    ModelFoundation,
    description="Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.",
    persistent="persistent",
    relationships=(
        Relationship(
            name="account_group",
            description="Belongs to one Account Group through `group_id`.",
            definition=AccountGroup,
            cardinality="1",
            optional=False,
        ),
        Relationship(
            name="broker",
            description="Belongs to one Broker through `broker_id`.",
            definition=Broker,
            cardinality="1",
            optional=False,
        ),
        Relationship(
            name="instance",
            description="Uses one Instance through `instance_id`.",
            definition=Instance,
            cardinality="1",
            optional=False,
        ),
        Relationship(
            name="base_currency",
            description="Uses one Currency as its base currency through `base_currency_id`.",
            definition=Currency,
            cardinality="1",
            optional=False,
        ),
    ),
    composite_constraints=(
        Constraint(
            id="account_group_id_broker_id_instance_id_unique",
            description="The combination of `group_id`, `broker_id`, and `instance_id` must be unique.",
        ),
    ),
):
    id: Annotated[
        int,
        Declare(
            description="The unique identity of the account.",
            logical_type="integer",
            identity=True,
            generated=True,
        ),
    ]
    name: Annotated[
        str,
        Declare(
            description="The account's display name.",
            logical_type="string",
            unique=True,
        ),
    ]
    group_id: Annotated[
        int,
        Declare(
            description="Identifies the account group that contains the account.",
            logical_type="integer",
        ),
    ]
    broker_id: Annotated[
        int,
        Declare(
            description="Identifies the broker that owns the account.",
            logical_type="integer",
        ),
    ]
    instance_id: Annotated[
        int,
        Declare(
            description="Identifies the trading-platform instance used to connect this account.",
            logical_type="integer",
        ),
    ]
    base_currency_id: Annotated[
        int,
        Declare(
            description="Identifies the base currency used by the account.",
            logical_type="integer",
        ),
    ]
    username: Annotated[
        str,
        Declare(
            description="The username identifier used to access the trading account.",
            logical_type="string",
        ),
    ]
    password: Annotated[
        str,
        Declare(
            description="The credential used to access the trading account.",
            logical_type="string",
            sensitivity=Sensitivity(classification="credential", at_rest="encrypted"),
        ),
    ]
    leverage: Annotated[
        int,
        Declare(
            description="Defines the account's leverage multiplier.",
            logical_type="integer",
        ),
    ]
    balance: Annotated[
        ExactDecimal,
        Declare(
            description="Stores the account's current balance.", logical_type="decimal"
        ),
    ] = Decimal(0)
    account_type: Annotated[
        str,
        Declare(
            description="Identifies the account model, such as `cfd` or `spread_betting`.",
            logical_type="string",
        ),
    ]
    is_active: Annotated[
        bool,
        Declare(
            description="Indicates whether the account is active.",
            logical_type="boolean",
        ),
    ] = True
    description: Annotated[
        str | None, Declare(description="Describes the account.", logical_type="string")
    ]
