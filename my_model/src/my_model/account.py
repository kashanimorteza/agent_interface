"""The Account domain entity."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from ._base import GENERATE_SECURELY, BaseModel


class Account(BaseModel):
    """A funded trading account through which the system executes trades and
    launches positions, identifying its account-level login credentials while its
    selected Instance owns the separate technical Trading Platform connection.
    """

    credential_fields = frozenset({"password"})
    initial_data = (
        {
            "name": "Acc-1",
            "group_id": 1,
            "broker_id": 1,
            "instance_id": 1,
            "base_currency_id": 1,
            "username": "test",
            "password": GENERATE_SECURELY,
            "leverage": 100,
            "account_type": "CFD",
        },
    )

    id: int | None = Field(
        default=None, description="System-generated identity, absent until persisted."
    )
    name: str = Field(min_length=1, description="The account's unique display name.")
    group_id: int = Field(description="Identifies the account group that contains the account.")
    broker_id: int = Field(description="Identifies the broker that owns the account.")
    instance_id: int = Field(
        description="Identifies the trading-platform instance used to connect this account."
    )
    base_currency_id: int = Field(description="Identifies the base currency used by the account.")
    username: str = Field(
        min_length=1, description="The username identifier used to access the trading account."
    )
    password: str = Field(
        min_length=1, description="The credential used to access the trading account."
    )
    leverage: int = Field(gt=0, description="The account's leverage multiplier.")
    balance: Decimal = Field(default=Decimal("0"), description="The account's current balance.")
    account_type: str = Field(
        min_length=1, description="The account model, such as cfd or spread_betting."
    )
    status: bool = Field(default=True, description="Whether the account is active.")
    description: str | None = Field(default=None, description="Describes the account.")
