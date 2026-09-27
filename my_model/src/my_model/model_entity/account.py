"""The Account Entity."""

from decimal import Decimal
from typing import ClassVar

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from my_model.model_declaration import (
    FieldDeclaration,
    Model_Declaration,
    ReferenceDeclaration,
)
from my_model.model_foundation import Model_Foundation


class Account(Model_Foundation, table=True):
    """A funded trading account through which the system executes trades and launches positions."""

    declaration: ClassVar[Model_Declaration] = Model_Declaration(
        entity="Account",
        purpose="A funded trading account through which the system executes trades and launches positions.",
        fields=(
            FieldDeclaration(
                name="id",
                type="integer",
                nullable=False,
                value_generation="auto_increment",
            ),
            FieldDeclaration(
                name="name",
                type="string",
                nullable=False,
                purpose="The account's display name.",
            ),
            FieldDeclaration(
                name="group_id",
                type="integer",
                nullable=False,
                purpose="Identifies the account group that contains the account.",
            ),
            FieldDeclaration(
                name="broker_id",
                type="integer",
                nullable=False,
                purpose="Identifies the broker that owns the account.",
            ),
            FieldDeclaration(
                name="instance_id",
                type="integer",
                nullable=False,
                purpose="Identifies the trading-platform instance used to connect this account.",
            ),
            FieldDeclaration(
                name="base_currency_id",
                type="integer",
                nullable=False,
                purpose="Identifies the base currency used by the account.",
            ),
            FieldDeclaration(
                name="username",
                type="string",
                nullable=False,
                purpose="The username identifier used to access the trading account.",
            ),
            FieldDeclaration(
                name="password",
                type="string",
                nullable=False,
                purpose="The credential used to access the trading account.",
                sensitive=True,
            ),
            FieldDeclaration(
                name="leverage",
                type="integer",
                nullable=False,
                purpose="The account's leverage multiplier.",
            ),
            FieldDeclaration(
                name="balance",
                type="decimal",
                nullable=False,
                purpose="The account's current balance.",
                has_default=True,
                default=Decimal(0),
            ),
            FieldDeclaration(
                name="account_type",
                type="string",
                nullable=False,
                purpose="Identifies the account model, such as cfd or spread_betting.",
            ),
            FieldDeclaration(
                name="is_active",
                type="boolean",
                nullable=False,
                purpose="Indicates whether the account is active.",
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type="string",
                nullable=True,
                purpose="Describes the account.",
            ),
        ),
        references=(
            ReferenceDeclaration(field="group_id", entity="AccountGroup"),
            ReferenceDeclaration(field="broker_id", entity="Broker"),
            ReferenceDeclaration(field="instance_id", entity="Instance"),
            ReferenceDeclaration(field="base_currency_id", entity="Currency"),
        ),
        unique_constraints=(
            ("name",),
            ("group_id", "broker_id", "instance_id"),
        ),
    )
    __table_args__ = (UniqueConstraint("group_id", "broker_id", "instance_id"),)

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    group_id: int = Field(foreign_key="accountgroup.id")
    broker_id: int = Field(foreign_key="broker.id")
    instance_id: int = Field(foreign_key="instance.id")
    base_currency_id: int = Field(foreign_key="currency.id")
    username: str
    password: str
    leverage: int
    balance: Decimal = Decimal(0)
    account_type: str
    is_active: bool = True
    description: str | None = None
