"""The Account Entity."""

from decimal import Decimal
from typing import ClassVar

from sqlmodel import Field
from sqlmodel import UniqueConstraint as TableUniqueConstraint

from model.core.base import Entity
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniqueConstraint,
    ValueGeneration,
)


class Account(Entity, table=True):
    """The Account Entity."""

    declaration: ClassVar[Declaration] = Declaration(
        name="Account",
        description="Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.",
        fields=(
            FieldDeclaration(
                name="id",
                type=FieldType.INTEGER,
                nullable=False,
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
                has_default=True,
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
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type=FieldType.STRING,
                nullable=True,
                description="Describes the account.",
            ),
        ),
        primary_key="id",
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
            UniqueConstraint(fields=("name",)),
            UniqueConstraint(fields=("group_id", "broker_id", "instance_id")),
        ),
    )

    __table_args__ = (TableUniqueConstraint("group_id", "broker_id", "instance_id"),)

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
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
