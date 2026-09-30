"""The Account Entity."""

from decimal import Decimal
from typing import ClassVar

from model.core.declaration import Declaration, FieldDeclaration, Relation
from model.core.foundation import Foundation


class Account(Foundation):
    declaration: ClassVar[Declaration] = Declaration(
        name="Account",
        description="Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.",
        fields=(
            FieldDeclaration(
                name="id",
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
                default=Decimal("0"),
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
    balance: Decimal = Decimal("0")
    account_type: str
    is_active: bool = True
    description: str | None = None
