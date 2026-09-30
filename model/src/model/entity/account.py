"""The Account Entity."""

from decimal import Decimal
from typing import ClassVar

from ..core.base import EntityBase
from ..core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    Sensitivity,
    ValueGeneration,
)


class Account(EntityBase):
    """The Account Entity; its Declaration states its complete meaning."""

    declaration: ClassVar[Declaration] = Declaration(
        name="Account",
        description="Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.",
        fields=(
            FieldDeclaration(
                name="id",
                description=None,
                type=FieldType.INTEGER,
                nullable=False,
                immutable=True,
                value_generation=ValueGeneration.AUTO_INCREMENT,
            ),
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
                sensitivity=Sensitivity.PASSWORD,
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
                has_default=True,
                default=Decimal(0),
            ),
            FieldDeclaration(
                name="account_type",
                description="Identifies the account model, such as `cfd` or `spread_betting`.",
                type=FieldType.STRING,
                nullable=False,
            ),
            FieldDeclaration(
                name="is_active",
                description="Indicates whether the account is active.",
                type=FieldType.BOOLEAN,
                nullable=False,
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                description="Describes the account.",
                type=FieldType.STRING,
                nullable=True,
            ),
        ),
        primary_key="id",
        relations=(
            Relation("group_id", "Account Group", "id"),
            Relation("broker_id", "Broker", "id"),
            Relation("instance_id", "Instance", "id"),
            Relation("base_currency_id", "Currency", "id"),
        ),
        unique_constraints=(
            ("name",),
            ("group_id", "broker_id", "instance_id"),
        ),
    )

    id: int | None = None
    name: str
    group_id: int
    broker_id: int
    instance_id: int
    base_currency_id: int
    username: str
    password: str
    leverage: int
    balance: Decimal = Decimal(0)
    account_type: str
    is_active: bool = True
    description: str | None = None
