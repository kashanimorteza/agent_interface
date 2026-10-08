"""Account Entity."""

from decimal import Decimal
from typing import ClassVar

from model.core import _storage as storage
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    Sensitivity,
    ValueGeneration,
)
from model.core.foundation import Foundation


class Account(Foundation, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="Account",
        description="Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.",
        primary_key="id",
        fields=(
            FieldDeclaration(
                name="id",
                type=FieldType.integer,
                nullable=False,
                immutable=True,
                value_generation=ValueGeneration.auto_increment,
            ),
            FieldDeclaration(
                name="name",
                type=FieldType.string,
                nullable=False,
                description="The account's display name.",
            ),
            FieldDeclaration(
                name="group_id",
                type=FieldType.integer,
                nullable=False,
                description="Identifies the account group that contains the account.",
            ),
            FieldDeclaration(
                name="broker_id",
                type=FieldType.integer,
                nullable=False,
                description="Identifies the broker that owns the account.",
            ),
            FieldDeclaration(
                name="instance_id",
                type=FieldType.integer,
                nullable=False,
                description="Identifies the trading-platform instance used to connect this account.",
            ),
            FieldDeclaration(
                name="base_currency_id",
                type=FieldType.integer,
                nullable=False,
                description="Identifies the base currency used by the account.",
            ),
            FieldDeclaration(
                name="username",
                type=FieldType.string,
                nullable=False,
                description="The username identifier used to access the trading account.",
            ),
            FieldDeclaration(
                name="password",
                type=FieldType.string,
                nullable=False,
                description="The credential used to access the trading account.",
                sensitivity=Sensitivity.password,
            ),
            FieldDeclaration(
                name="leverage",
                type=FieldType.integer,
                nullable=False,
                description="Defines the account's leverage multiplier.",
            ),
            FieldDeclaration(
                name="balance",
                type=FieldType.decimal,
                nullable=False,
                description="Stores the account's current balance.",
                default=Decimal(0),
            ),
            FieldDeclaration(
                name="account_type",
                type=FieldType.string,
                nullable=False,
                description="Identifies the account model, such as `cfd` or `spread_betting`.",
            ),
            FieldDeclaration(
                name="is_active",
                type=FieldType.boolean,
                nullable=False,
                description="Indicates whether the account is active.",
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type=FieldType.string,
                nullable=True,
                description="Describes the account.",
            ),
        ),
        relations=(
            Relation(
                local_field="group_id", target_entity="Account Group", target_field="id"
            ),
            Relation(
                local_field="broker_id", target_entity="Broker", target_field="id"
            ),
            Relation(
                local_field="instance_id", target_entity="Instance", target_field="id"
            ),
            Relation(
                local_field="base_currency_id",
                target_entity="Currency",
                target_field="id",
            ),
        ),
        unique_constraints=(
            ("name",),
            ("group_id", "broker_id", "instance_id"),
        ),
    )
    __tablename__ = "Account"
    __table_args__ = storage.table_args(declaration)

    id: int | None = storage.field(declaration, "id")
    name: str = storage.field(declaration, "name")
    group_id: int = storage.field(declaration, "group_id")
    broker_id: int = storage.field(declaration, "broker_id")
    instance_id: int = storage.field(declaration, "instance_id")
    base_currency_id: int = storage.field(declaration, "base_currency_id")
    username: str = storage.field(declaration, "username")
    password: str = storage.field(declaration, "password")
    leverage: int = storage.field(declaration, "leverage")
    balance: Decimal = storage.field(declaration, "balance")
    account_type: str = storage.field(declaration, "account_type")
    is_active: bool = storage.field(declaration, "is_active")
    description: str | None = storage.field(declaration, "description")
