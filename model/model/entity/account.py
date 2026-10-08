"""The Account Entity."""

from decimal import Decimal
from typing import ClassVar

from model.core._storage import realize_field, table_args
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    ValueGeneration,
)
from model.core.foundation import Foundation


class Account(Foundation, table=True):
    __tablename__ = "Account"
    declaration: ClassVar[Declaration] = Declaration(
        name="Account",
        description="Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.",
        fields=(
            FieldDeclaration(
                "id",
                FieldType.integer,
                False,
                immutable=True,
                value_generation=ValueGeneration.auto_increment,
            ),
            FieldDeclaration(
                "name",
                FieldType.string,
                False,
                description="The account's display name.",
            ),
            FieldDeclaration(
                "group_id",
                FieldType.integer,
                False,
                description="Identifies the account group that contains the account.",
            ),
            FieldDeclaration(
                "broker_id",
                FieldType.integer,
                False,
                description="Identifies the broker that owns the account.",
            ),
            FieldDeclaration(
                "instance_id",
                FieldType.integer,
                False,
                description="Identifies the trading-platform instance used to connect this account.",
            ),
            FieldDeclaration(
                "base_currency_id",
                FieldType.integer,
                False,
                description="Identifies the base currency used by the account.",
            ),
            FieldDeclaration(
                "username",
                FieldType.string,
                False,
                description="The username identifier used to access the trading account.",
            ),
            FieldDeclaration(
                "password",
                FieldType.string,
                False,
                description="The credential used to access the trading account.",
            ),
            FieldDeclaration(
                "leverage",
                FieldType.integer,
                False,
                description="Defines the account's leverage multiplier.",
            ),
            FieldDeclaration(
                "balance",
                FieldType.decimal,
                False,
                description="Stores the account's current balance.",
                default=Decimal(0),
            ),
            FieldDeclaration(
                "account_type",
                FieldType.string,
                False,
                description="Identifies the account model, such as `cfd` or `spread_betting`.",
            ),
            FieldDeclaration(
                "is_active",
                FieldType.boolean,
                False,
                description="Indicates whether the account is active.",
                default=True,
            ),
            FieldDeclaration(
                "description",
                FieldType.string,
                True,
                description="Describes the account.",
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
    __table_args__ = table_args(declaration)

    id: int | None = realize_field(declaration, "id")
    name: str = realize_field(declaration, "name")
    group_id: int = realize_field(declaration, "group_id")
    broker_id: int = realize_field(declaration, "broker_id")
    instance_id: int = realize_field(declaration, "instance_id")
    base_currency_id: int = realize_field(declaration, "base_currency_id")
    username: str = realize_field(declaration, "username")
    password: str = realize_field(declaration, "password")
    leverage: int = realize_field(declaration, "leverage")
    balance: Decimal = realize_field(declaration, "balance")
    account_type: str = realize_field(declaration, "account_type")
    is_active: bool = realize_field(declaration, "is_active")
    description: str | None = realize_field(declaration, "description")
