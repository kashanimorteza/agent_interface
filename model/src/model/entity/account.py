"""The Account Entity."""

from decimal import Decimal
from typing import ClassVar

from model.core._entity import Entity
from model.core._fields import activity, identity
from model.core._types import DecimalValue
from model.core.declaration import Declaration as EntityDeclaration
from model.core.declaration import FieldDeclaration, Relation


class Account(Entity):
    Declaration: ClassVar[EntityDeclaration] = EntityDeclaration(
        name="Account",
        description=(
            "Defines a funded trading account through which the "
            "system executes trades and launches positions. Each "
            "Account identifies the trading account and its "
            "account-level login credentials, while its selected "
            "Instance owns the separate technical connection to "
            "the Trading Platform."
        ),
        fields=(
            identity(),
            FieldDeclaration(
                "name",
                "string",
                nullable=False,
                description="The account's display name.",
            ),
            FieldDeclaration(
                "group_id",
                "integer",
                nullable=False,
                description=("Identifies the account group that contains the account."),
            ),
            FieldDeclaration(
                "broker_id",
                "integer",
                nullable=False,
                description="Identifies the broker that owns the account.",
            ),
            FieldDeclaration(
                "instance_id",
                "integer",
                nullable=False,
                description=(
                    "Identifies the trading-platform instance used to "
                    "connect this account."
                ),
            ),
            FieldDeclaration(
                "base_currency_id",
                "integer",
                nullable=False,
                description="Identifies the base currency used by the account.",
            ),
            FieldDeclaration(
                "username",
                "string",
                nullable=False,
                description=(
                    "The username identifier used to access the trading account."
                ),
            ),
            FieldDeclaration(
                "password",
                "string",
                nullable=False,
                description="The credential used to access the trading account.",
                sensitivity="password",
            ),
            FieldDeclaration(
                "leverage",
                "integer",
                nullable=False,
                description="Defines the account's leverage multiplier.",
            ),
            FieldDeclaration(
                "balance",
                "decimal",
                nullable=False,
                description="Stores the account's current balance.",
                has_default=True,
                default=Decimal("0"),
            ),
            FieldDeclaration(
                "account_type",
                "string",
                nullable=False,
                description=(
                    "Identifies the account model, such as `cfd` or `spread_betting`."
                ),
            ),
            activity("Indicates whether the account is active."),
            FieldDeclaration(
                "description",
                "string",
                nullable=True,
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

    id: int | None = None
    name: str
    group_id: int
    broker_id: int
    instance_id: int
    base_currency_id: int
    username: str
    password: str
    leverage: int
    balance: DecimalValue = Decimal("0")
    account_type: str
    is_active: bool = True
    description: str | None = None
