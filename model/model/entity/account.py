"""The Account Entity."""

from decimal import Decimal
from typing import ClassVar

from model.core._storage import column, table_args
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniqueConstraint,
    ValueGeneration,
)
from model.core.foundation import Foundation

_DECLARATION = Declaration(
    name="Account",
    description=(
        "Defines a funded trading account through which the system executes "
        "trades and launches positions. Each Account identifies the trading "
        "account and its account-level login credentials, while its selected "
        "Instance owns the separate technical connection to the Trading "
        "Platform."
    ),
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
            has_default=True,
            default=Decimal("0"),
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
            has_default=True,
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
        Relation(local_field="group_id", target_entity="Account Group", target_field="id"),
        Relation(local_field="broker_id", target_entity="Broker", target_field="id"),
        Relation(local_field="instance_id", target_entity="Instance", target_field="id"),
        Relation(local_field="base_currency_id", target_entity="Currency", target_field="id"),
    ),
    unique_constraints=(
        UniqueConstraint(fields=("name",)),
        UniqueConstraint(fields=("group_id", "broker_id", "instance_id")),
    ),
)


class Account(Foundation, table=True):
    """Account."""

    __tablename__ = "Account"  # pyright: ignore[reportAssignmentType]
    declaration: ClassVar[Declaration] = _DECLARATION
    __table_args__ = table_args(_DECLARATION)

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
