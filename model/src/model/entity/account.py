from decimal import Decimal
from typing import ClassVar

from model.core.base import Entity
from model.core.columns import column, table_arguments
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    RelationDeclaration,
    UniqueConstraintDeclaration,
    activity,
    identity,
)

_DECLARATION = Declaration(
    name="Account",
    description="Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.",
    fields=(
        identity(),
        FieldDeclaration(
            name="name",
            description="The account's display name.",
            type=FieldType.STRING,
            nullable=False,
        ),
        FieldDeclaration(
            name="group_id",
            description="Identifies the account group that contains the account.",
            type=FieldType.INTEGER,
            nullable=False,
        ),
        FieldDeclaration(
            name="broker_id",
            description="Identifies the broker that owns the account.",
            type=FieldType.INTEGER,
            nullable=False,
        ),
        FieldDeclaration(
            name="instance_id",
            description="Identifies the trading-platform instance used to connect this account.",
            type=FieldType.INTEGER,
            nullable=False,
        ),
        FieldDeclaration(
            name="base_currency_id",
            description="Identifies the base currency used by the account.",
            type=FieldType.INTEGER,
            nullable=False,
        ),
        FieldDeclaration(
            name="username",
            description="The username identifier used to access the trading account.",
            type=FieldType.STRING,
            nullable=False,
        ),
        FieldDeclaration(
            name="password",
            description="The credential used to access the trading account.",
            type=FieldType.STRING,
            nullable=False,
        ),
        FieldDeclaration(
            name="leverage",
            description="Defines the account's leverage multiplier.",
            type=FieldType.INTEGER,
            nullable=False,
        ),
        FieldDeclaration(
            name="balance",
            description="Stores the account's current balance.",
            type=FieldType.DECIMAL,
            nullable=False,
            default=Decimal(0),
        ),
        FieldDeclaration(
            name="account_type",
            description="Identifies the account model, such as `cfd` or `spread_betting`.",
            type=FieldType.STRING,
            nullable=False,
        ),
        activity("Indicates whether the account is active."),
        FieldDeclaration(
            name="description",
            description="Describes the account.",
            type=FieldType.STRING,
            nullable=True,
        ),
    ),
    primary_key="id",
    relations=(
        RelationDeclaration("group_id", "Account Group", "id"),
        RelationDeclaration("broker_id", "Broker", "id"),
        RelationDeclaration("instance_id", "Instance", "id"),
        RelationDeclaration("base_currency_id", "Currency", "id"),
    ),
    unique_constraints=(
        UniqueConstraintDeclaration(("name",)),
        UniqueConstraintDeclaration(
            (
                "group_id",
                "broker_id",
                "instance_id",
            )
        ),
    ),
)


class Account(Entity, table=True):
    __table_args__ = table_arguments(_DECLARATION)
    declaration: ClassVar[Declaration] = _DECLARATION

    id: int | None = column(_DECLARATION, "id")
    name: str = column(_DECLARATION, "name")
    group_id: int = column(_DECLARATION, "group_id")
    broker_id: int = column(_DECLARATION, "broker_id")
    instance_id: int = column(_DECLARATION, "instance_id")
    base_currency_id: int = column(_DECLARATION, "base_currency_id")
    username: str = column(_DECLARATION, "username")
    password: str = column(_DECLARATION, "password")
    leverage: int = column(_DECLARATION, "leverage")
    balance: Decimal = column(_DECLARATION, "balance")
    account_type: str = column(_DECLARATION, "account_type")
    is_active: bool = column(_DECLARATION, "is_active")
    description: str | None = column(_DECLARATION, "description")
