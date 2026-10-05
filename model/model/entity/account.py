from decimal import Decimal
from typing import ClassVar

from sqlalchemy import Identity, UniqueConstraint
from sqlmodel import Field

from model.core._base import EntityBase
from model.core._columns import DecimalText
from model.core.declaration import Declaration, FieldDeclaration, Relation


class Account(EntityBase, table=True):
    __table_args__ = (
        UniqueConstraint("group_id", "broker_id", "instance_id"),
        {"sqlite_autoincrement": True},
    )
    declaration: ClassVar[Declaration] = Declaration(
        "Account",
        "Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.",
        (
            FieldDeclaration("id", None, "integer", False, immutable=True, value_generation="auto_increment"),
            FieldDeclaration("name", "The account's display name.", "string", False),
            FieldDeclaration("group_id", "Identifies the account group that contains the account.", "integer", False),
            FieldDeclaration("broker_id", "Identifies the broker that owns the account.", "integer", False),
            FieldDeclaration(
                "instance_id",
                "Identifies the trading-platform instance used to connect this account.",
                "integer",
                False,
            ),
            FieldDeclaration("base_currency_id", "Identifies the base currency used by the account.", "integer", False),
            FieldDeclaration(
                "username", "The username identifier used to access the trading account.", "string", False
            ),
            FieldDeclaration("password", "The credential used to access the trading account.", "string", False),
            FieldDeclaration("leverage", "Defines the account's leverage multiplier.", "integer", False),
            FieldDeclaration(
                "balance",
                "Stores the account's current balance.",
                "decimal",
                False,
                has_default=True,
                default=Decimal("0"),
            ),
            FieldDeclaration(
                "account_type", "Identifies the account model, such as `cfd` or `spread_betting`.", "string", False
            ),
            FieldDeclaration(
                "is_active",
                "Indicates whether the account is active.",
                "boolean",
                False,
                has_default=True,
                default=True,
            ),
            FieldDeclaration("description", "Describes the account.", "string", True),
        ),
        "id",
        relations=(
            Relation("group_id", "Account Group", "id"),
            Relation("broker_id", "Broker", "id"),
            Relation("instance_id", "Instance", "id"),
            Relation("base_currency_id", "Currency", "id"),
        ),
        unique_constraints=(
            ("name",),
            (
                "group_id",
                "broker_id",
                "instance_id",
            ),
        ),
    )
    id: int | None = Field(default=None, primary_key=True, sa_column_args=[Identity()])
    name: str = Field(unique=True, description="The account's display name.")
    group_id: int = Field(
        foreign_key="AccountGroup.id", description="Identifies the account group that contains the account."
    )
    broker_id: int = Field(foreign_key="Broker.id", description="Identifies the broker that owns the account.")
    instance_id: int = Field(
        foreign_key="Instance.id", description="Identifies the trading-platform instance used to connect this account."
    )
    base_currency_id: int = Field(
        foreign_key="Currency.id", description="Identifies the base currency used by the account."
    )
    username: str = Field(description="The username identifier used to access the trading account.")
    password: str = Field(description="The credential used to access the trading account.")
    leverage: int = Field(description="Defines the account's leverage multiplier.")
    balance: Decimal = Field(
        default=Decimal("0"), sa_type=DecimalText, description="Stores the account's current balance."
    )
    account_type: str = Field(description="Identifies the account model, such as `cfd` or `spread_betting`.")
    is_active: bool = Field(default=True, description="Indicates whether the account is active.")
    description: str | None = Field(default=None, description="Describes the account.")
