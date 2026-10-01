"""The Account Entity."""

from decimal import Decimal
from typing import ClassVar

from sqlmodel import Field

from model.core.base import Entity
from model.core.declaration import Declaration, FieldDeclaration, Relation
from model.core.storage import column_options, table_args

_DECLARATION = Declaration(
    name="Account",
    description="Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.",
    fields=(
        FieldDeclaration(
            name="id",
            description=None,
            type="integer",
            nullable=False,
            immutable=True,
            value_generation="auto_increment",
        ),
        FieldDeclaration(
            name="name",
            description="The account's display name.",
            type="string",
            nullable=False,
        ),
        FieldDeclaration(
            name="group_id",
            description="Identifies the account group that contains the account.",
            type="integer",
            nullable=False,
        ),
        FieldDeclaration(
            name="broker_id",
            description="Identifies the broker that owns the account.",
            type="integer",
            nullable=False,
        ),
        FieldDeclaration(
            name="instance_id",
            description="Identifies the trading-platform instance used to connect this account.",
            type="integer",
            nullable=False,
        ),
        FieldDeclaration(
            name="base_currency_id",
            description="Identifies the base currency used by the account.",
            type="integer",
            nullable=False,
        ),
        FieldDeclaration(
            name="username",
            description="The username identifier used to access the trading account.",
            type="string",
            nullable=False,
        ),
        FieldDeclaration(
            name="password",
            description="The credential used to access the trading account.",
            type="string",
            nullable=False,
            sensitivity="password",
        ),
        FieldDeclaration(
            name="leverage",
            description="Defines the account's leverage multiplier.",
            type="integer",
            nullable=False,
        ),
        FieldDeclaration(
            name="balance",
            description="Stores the account's current balance.",
            type="decimal",
            nullable=False,
            has_default=True,
            default=Decimal(0),
        ),
        FieldDeclaration(
            name="account_type",
            description="Identifies the account model, such as `cfd` or `spread_betting`.",
            type="string",
            nullable=False,
        ),
        FieldDeclaration(
            name="is_active",
            description="Indicates whether the account is active.",
            type="boolean",
            nullable=False,
            has_default=True,
            default=True,
        ),
        FieldDeclaration(
            name="description",
            description="Describes the account.",
            type="string",
            nullable=True,
        ),
    ),
    primary_key="id",
    relations=(
        Relation(
            local_field="group_id", target_entity="Account Group", target_field="id"
        ),
        Relation(local_field="broker_id", target_entity="Broker", target_field="id"),
        Relation(
            local_field="instance_id", target_entity="Instance", target_field="id"
        ),
        Relation(
            local_field="base_currency_id", target_entity="Currency", target_field="id"
        ),
    ),
    unique_constraints=(
        ("name",),
        ("group_id", "broker_id", "instance_id"),
    ),
    indexes=(),
)


class Account(Entity, table=True):
    __table_args__ = table_args(_DECLARATION)
    declaration: ClassVar[Declaration] = _DECLARATION

    id: int | None = Field(default=None, **column_options(_DECLARATION, "id"))
    name: str = Field(
        description="The account's display name.",
        **column_options(_DECLARATION, "name"),
    )
    group_id: int = Field(
        description="Identifies the account group that contains the account.",
        **column_options(_DECLARATION, "group_id"),
    )
    broker_id: int = Field(
        description="Identifies the broker that owns the account.",
        **column_options(_DECLARATION, "broker_id"),
    )
    instance_id: int = Field(
        description="Identifies the trading-platform instance used to connect this account.",
        **column_options(_DECLARATION, "instance_id"),
    )
    base_currency_id: int = Field(
        description="Identifies the base currency used by the account.",
        **column_options(_DECLARATION, "base_currency_id"),
    )
    username: str = Field(
        description="The username identifier used to access the trading account.",
        **column_options(_DECLARATION, "username"),
    )
    password: str = Field(
        description="The credential used to access the trading account.",
        **column_options(_DECLARATION, "password"),
    )
    leverage: int = Field(
        description="Defines the account's leverage multiplier.",
        **column_options(_DECLARATION, "leverage"),
    )
    balance: Decimal = Field(
        default=Decimal(0),
        description="Stores the account's current balance.",
        **column_options(_DECLARATION, "balance"),
    )
    account_type: str = Field(
        description="Identifies the account model, such as `cfd` or `spread_betting`.",
        **column_options(_DECLARATION, "account_type"),
    )
    is_active: bool = Field(
        default=True,
        description="Indicates whether the account is active.",
        **column_options(_DECLARATION, "is_active"),
    )
    description: str | None = Field(
        default=None,
        description="Describes the account.",
        **column_options(_DECLARATION, "description"),
    )
