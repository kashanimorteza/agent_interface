"""The Account Entity."""

from decimal import Decimal
from typing import ClassVar

from model.core._storage import realize_field, table_args
from model.core.declaration import (
    EntityDeclaration,
    FieldDeclaration,
    FieldType,
    Relation,
    Sensitivity,
    UniqueConstraint,
    ValueGeneration,
)
from model.core.foundation import Foundation

DECLARATION = EntityDeclaration(
    name="Account",
    description="Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.",
    fields=(
        FieldDeclaration(
            "id",
            FieldType.integer,
            nullable=False,
            immutable=True,
            value_generation=ValueGeneration.auto_increment,
        ),
        FieldDeclaration(
            "name",
            FieldType.string,
            nullable=False,
            description="The account's display name.",
        ),
        FieldDeclaration(
            "group_id",
            FieldType.integer,
            nullable=False,
            description="Identifies the account group that contains the account.",
        ),
        FieldDeclaration(
            "broker_id",
            FieldType.integer,
            nullable=False,
            description="Identifies the broker that owns the account.",
        ),
        FieldDeclaration(
            "instance_id",
            FieldType.integer,
            nullable=False,
            description="Identifies the trading-platform instance used to connect this account.",
        ),
        FieldDeclaration(
            "base_currency_id",
            FieldType.integer,
            nullable=False,
            description="Identifies the base currency used by the account.",
        ),
        FieldDeclaration(
            "username",
            FieldType.string,
            nullable=False,
            description="The username identifier used to access the trading account.",
        ),
        FieldDeclaration(
            "password",
            FieldType.string,
            nullable=False,
            description="The credential used to access the trading account.",
            sensitivity=Sensitivity.password,
        ),
        FieldDeclaration(
            "leverage",
            FieldType.integer,
            nullable=False,
            description="Defines the account's leverage multiplier.",
        ),
        FieldDeclaration(
            "balance",
            FieldType.decimal,
            nullable=False,
            description="Stores the account's current balance.",
            default=Decimal(0),
        ),
        FieldDeclaration(
            "account_type",
            FieldType.string,
            nullable=False,
            description="Identifies the account model, such as `cfd` or `spread_betting`.",
        ),
        FieldDeclaration(
            "is_active",
            FieldType.boolean,
            nullable=False,
            description="Indicates whether the account is active.",
            default=True,
        ),
        FieldDeclaration(
            "description",
            FieldType.string,
            nullable=True,
            description="Describes the account.",
        ),
    ),
    relations=(
        Relation("group_id", "Account Group", "id"),
        Relation("broker_id", "Broker", "id"),
        Relation("instance_id", "Instance", "id"),
        Relation("base_currency_id", "Currency", "id"),
    ),
    unique_constraints=(
        UniqueConstraint(("name",)),
        UniqueConstraint(("group_id", "broker_id", "instance_id")),
    ),
)


class Account(Foundation, table=True):
    __tablename__ = "Account"
    __table_args__ = table_args(DECLARATION)

    declaration: ClassVar[EntityDeclaration] = DECLARATION

    id: int | None = realize_field(DECLARATION, "id")
    name: str = realize_field(DECLARATION, "name")
    group_id: int = realize_field(DECLARATION, "group_id")
    broker_id: int = realize_field(DECLARATION, "broker_id")
    instance_id: int = realize_field(DECLARATION, "instance_id")
    base_currency_id: int = realize_field(DECLARATION, "base_currency_id")
    username: str = realize_field(DECLARATION, "username")
    password: str = realize_field(DECLARATION, "password")
    leverage: int = realize_field(DECLARATION, "leverage")
    balance: Decimal = realize_field(DECLARATION, "balance")
    account_type: str = realize_field(DECLARATION, "account_type")
    is_active: bool = realize_field(DECLARATION, "is_active")
    description: str | None = realize_field(DECLARATION, "description")
