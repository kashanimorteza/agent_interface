"""Account Entity."""

from decimal import Decimal
from typing import ClassVar

from ..core._storage import realize_field, table_arguments, table_name
from ..core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniquenessConstraint,
    ValueGeneration,
)
from ..core.foundation import Foundation

DECLARATION = Declaration(
    name="Account",
    description="Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.",
    fields=(
        FieldDeclaration(
            name="id",
            type=FieldType.integer,
            nullable=False,
            description=None,
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
        UniquenessConstraint(fields=("name",)),
        UniquenessConstraint(fields=("group_id", "broker_id", "instance_id")),
    ),
)


class Account(Foundation, table=True):
    __tablename__ = table_name(DECLARATION)
    __table_args__ = table_arguments(DECLARATION)

    declaration: ClassVar[Declaration] = DECLARATION

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
