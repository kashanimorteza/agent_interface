"""A funded trading account through which the system executes trades and launches positions."""

from __future__ import annotations

from decimal import Decimal
from typing import Any

from pydantic import Field

from ._base import DomainModel, credential_field
from ._generation import GENERATE_SECURELY


class Account(DomainModel):
    """A funded account, identifying its own login credentials separately from its Instance's technical connection.

    Instance credentials authenticate the technical Trading Platform
    connection; this Model's own credentials authenticate the trading
    account itself. Whether the same credential value is improperly
    duplicated across an Account and its referenced Instance depends on
    both records and the selected Trading Platform's requirements, so that
    check is out of this Model's own reach and belongs to Backend Logic.
    """

    unique_together = (("group_id", "broker_id", "instance_id"),)

    id: int | None = Field(default=None, description="Primary key, auto-incremented.")
    name: str = Field(description="The account's display name.", json_schema_extra={"unique": True})
    group_id: int = Field(description="Identifies the account group that contains the account.")
    broker_id: int = Field(description="Identifies the broker that owns the account.")
    instance_id: int = Field(description="Identifies the trading-platform instance used to connect this account.")
    base_currency_id: int = Field(description="Identifies the base currency used by the account.")
    username: str = Field(description="The username identifier used to access the trading account.")
    password: str = credential_field(description="The credential used to access the trading account.")
    leverage: int = Field(description="Defines the account's leverage multiplier.")
    balance: Decimal = Field(default=Decimal(0), description="Stores the account's current balance.")
    account_type: str = Field(description="Identifies the account model, such as cfd or spread_betting.")
    status: bool = Field(default=True, description="Indicates whether the account is active.")
    description: str | None = Field(default=None, description="Describes the account.")


INITIAL_DATA: tuple[dict[str, Any], ...] = (
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
