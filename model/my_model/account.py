"""Account: a funded trading account."""

from __future__ import annotations

from decimal import Decimal

from .account_group import AccountGroup
from .base import CredentialStorage, Model, Pending, Relationship, field
from .broker import Broker
from .currency import Currency


class Account(Model):
    """Defines a funded trading account through which the system executes
    trades and launches positions. Each account identifies its broker, account
    model, and login credentials so the system knows where the trade must be
    sent, how it must connect, and which account must be used for the
    operation."""

    id: int | None = field("integer", primary_key=True, auto_increment=True)
    name: str = field("string", unique=True, purpose="The account's display name.")
    group_id: int = field("integer", purpose="Identifies the account group that contains the account.")
    broker_id: int = field("integer", purpose="Identifies the broker that owns the account.")
    base_currency_id: int = field(
        "integer", purpose="Identifies the base currency used by the account."
    )
    username: str = field(
        "string", purpose="The username identifier used to access the trading account."
    )
    password: str = field(
        "string",
        credential=True,
        generated=True,
        purpose="The credential used to access the trading account.",
    )
    leverage: int = field("integer", purpose="Defines the account's leverage multiplier.")
    balance: Decimal = field(
        "decimal", default=Decimal("0"), purpose="Stores the account's current balance."
    )
    account_type: str = field(
        "string", purpose="Identifies the account model, such as cfd or spread_betting."
    )
    status: bool = field("boolean", default=True, purpose="Indicates whether the account is active.")
    description: str | None = field("string", nullable=True, purpose="Describes the account.")

    relationships = (
        Relationship(field="group_id", target=AccountGroup, kind="belongs_to"),
        Relationship(field="broker_id", target=Broker, kind="belongs_to"),
        Relationship(field="base_currency_id", target=Currency, kind="uses", role="base currency"),
    )

    rules = (CredentialStorage(field="password", mode="encrypted"),)

    initial_data = (
        {
            "name": "Acc-1",
            "group_id": 1,
            "broker_id": 1,
            "base_currency_id": 1,
            "username": "test",
            "password": Pending,
            "leverage": 100,
            "account_type": "CFD",
        },
    )
