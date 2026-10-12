"""The Account Entity."""

from decimal import Decimal
from typing import ClassVar

from model.core._storage import mapped_field, table_arguments
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    Sensitivity,
    UniquenessConstraint,
    ValueGeneration,
)
from model.core.foundation import Foundation


class Account(Foundation, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="Account",
        description=(
            "Defines a funded trading account through which the system executes trades and "
            "launches positions. Each Account identifies the trading account and its "
            "account-level login credentials, while its selected Instance owns the separate "
            "technical connection to the Trading Platform."
        ),
        fields=(
            FieldDeclaration(
                name="id",
                type=FieldType.INTEGER,
                nullable=False,
                immutable=True,
                value_generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration(
                name="name",
                type=FieldType.STRING,
                nullable=False,
                description="The account's display name.",
            ),
            FieldDeclaration(
                name="group_id",
                type=FieldType.INTEGER,
                nullable=False,
                description="Identifies the account group that contains the account.",
            ),
            FieldDeclaration(
                name="broker_id",
                type=FieldType.INTEGER,
                nullable=False,
                description="Identifies the broker that owns the account.",
            ),
            FieldDeclaration(
                name="instance_id",
                type=FieldType.INTEGER,
                nullable=False,
                description="Identifies the trading-platform instance used to connect this account.",
            ),
            FieldDeclaration(
                name="base_currency_id",
                type=FieldType.INTEGER,
                nullable=False,
                description="Identifies the base currency used by the account.",
            ),
            FieldDeclaration(
                name="username",
                type=FieldType.STRING,
                nullable=False,
                description="The username identifier used to access the trading account.",
            ),
            FieldDeclaration(
                name="password",
                type=FieldType.STRING,
                nullable=False,
                description="The credential used to access the trading account.",
                sensitivity=Sensitivity.PASSWORD,
            ),
            FieldDeclaration(
                name="leverage",
                type=FieldType.INTEGER,
                nullable=False,
                description="Defines the account's leverage multiplier.",
            ),
            FieldDeclaration(
                name="balance",
                type=FieldType.DECIMAL,
                nullable=False,
                description="Stores the account's current balance.",
                default=Decimal(0),
            ),
            FieldDeclaration(
                name="account_type",
                type=FieldType.STRING,
                nullable=False,
                description="Identifies the account model, such as `cfd` or `spread_betting`.",
            ),
            FieldDeclaration(
                name="is_active",
                type=FieldType.BOOLEAN,
                nullable=False,
                description="Indicates whether the account is active.",
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type=FieldType.STRING,
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
            UniquenessConstraint(("name",)),
            UniquenessConstraint(("group_id", "broker_id", "instance_id")),
        ),
    )

    __tablename__ = "Account"
    __table_args__ = table_arguments(declaration)

    id: int | None = mapped_field(declaration, "id")
    name: str = mapped_field(declaration, "name")
    group_id: int = mapped_field(declaration, "group_id")
    broker_id: int = mapped_field(declaration, "broker_id")
    instance_id: int = mapped_field(declaration, "instance_id")
    base_currency_id: int = mapped_field(declaration, "base_currency_id")
    username: str = mapped_field(declaration, "username")
    password: str = mapped_field(declaration, "password")
    leverage: int = mapped_field(declaration, "leverage")
    balance: Decimal = mapped_field(declaration, "balance")
    account_type: str = mapped_field(declaration, "account_type")
    is_active: bool = mapped_field(declaration, "is_active")
    description: str | None = mapped_field(declaration, "description")
