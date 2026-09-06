"""The Account Model."""

from decimal import Decimal
from collections.abc import Mapping
from typing import Annotated, ClassVar

from ._base import Model
from ._spec import FieldSpec, GenerateValue, LogicalType, RelationshipSpec, RuleSpec


class Account(Model):
    """Defines a funded trading account through which the system executes trades and launches
    positions. Each account identifies its broker, account model, and login credentials so the
    system knows where the trade must be sent, how it must connect, and which account must be used
    for the operation.
    """

    logical_key: ClassVar[str] = "account"
    logical_purpose: ClassVar[str] = (
        "Defines a funded trading account through which the system executes trades and launches positions. "
        "Each account identifies its broker, account model, and login credentials so the system knows where "
        "the trade must be sent, how it must connect, and which account must be used for the operation."
    )
    logical_relationships: ClassVar[tuple[RelationshipSpec, ...]] = (
        RelationshipSpec(name="account_group", type="belongs_to", target="account_group", field="account_group_id"),
        RelationshipSpec(name="broker", type="belongs_to", target="broker", field="broker_id"),
        RelationshipSpec(
            name="base_currency",
            type="uses",
            target="currency",
            field="base_currency_id",
            role="base currency",
        ),
    )
    logical_rules: ClassVar[tuple[RuleSpec, ...]] = (
        RuleSpec(
            rule="password is a credential and must use encrypted storage at rest.",
            kind="credential",
            field="password",
            storage="encrypted",
        ),
    )
    logical_initial_data: ClassVar[tuple[Mapping[str, object], ...]] = (
        {
            "name": "Acc-1",
            "account_group_id": 1,
            "broker_id": 1,
            "base_currency_id": 1,
            "username": "test",
            "password": GenerateValue("Generate securely"),
            "leverage": 100,
            "account_type": "CFD",
        },
    )

    id: Annotated[
        int | None,
        FieldSpec(
            type=LogicalType.integer,
            nullable=False,
            auto_increment=True,
            primary_key=True,
        ),
    ] = None
    name: Annotated[
        str,
        FieldSpec(
            type=LogicalType.string,
            nullable=False,
            unique=True,
            purpose="The account's display name.",
        ),
    ]
    account_group_id: Annotated[
        int,
        FieldSpec(
            type=LogicalType.integer,
            nullable=False,
            purpose="Identifies the account group that contains the account.",
        ),
    ]
    broker_id: Annotated[
        int,
        FieldSpec(
            type=LogicalType.integer,
            nullable=False,
            purpose="Identifies the broker that owns the account.",
        ),
    ]
    base_currency_id: Annotated[
        int,
        FieldSpec(
            type=LogicalType.integer,
            nullable=False,
            purpose="Identifies the base currency used by the account.",
        ),
    ]
    username: Annotated[
        str,
        FieldSpec(
            type=LogicalType.string,
            nullable=False,
            purpose="The username identifier used to access the trading account.",
        ),
    ]
    password: Annotated[
        str | None,
        FieldSpec(
            type=LogicalType.string,
            nullable=False,
            credential=True,
            purpose="The credential used to access the trading account.",
        ),
    ] = None
    leverage: Annotated[
        int,
        FieldSpec(
            type=LogicalType.integer,
            nullable=False,
            purpose="Defines the account's leverage multiplier.",
        ),
    ]
    balance: Annotated[
        Decimal,
        FieldSpec(
            type=LogicalType.decimal,
            nullable=False,
            default=0,
            purpose="Stores the account's current balance.",
        ),
    ] = Decimal("0")
    account_type: Annotated[
        str,
        FieldSpec(
            type=LogicalType.string,
            nullable=False,
            purpose="Identifies the account model, such as cfd or spread_betting.",
        ),
    ]
    status: Annotated[
        bool,
        FieldSpec(
            type=LogicalType.boolean,
            nullable=False,
            default=True,
            purpose="Indicates whether the account is active.",
        ),
    ] = True
    description: Annotated[
        str | None,
        FieldSpec(
            type=LogicalType.string,
            nullable=True,
            purpose="Describes the account.",
        ),
    ] = None
