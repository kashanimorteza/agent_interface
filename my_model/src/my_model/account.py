"""The Account domain entity: a funded trading account."""

from __future__ import annotations

from decimal import Decimal
from typing import Any, ClassVar

from pydantic import Field

from my_model._base import BaseModel
from my_model._initial_data import GENERATE_SECURELY


class Account(BaseModel):
    """A funded trading account through which the system executes trades and
    launches positions.

    Each Account identifies the trading account and its account-level login
    credentials, while its selected Instance owns the separate technical
    connection to the Trading Platform. Instance credentials authenticate
    the technical Trading Platform connection; Account credentials
    authenticate this specific trading account, and the two are kept as
    distinct fields so they are never confused with one another.
    """

    UNIQUE_TOGETHER: ClassVar[tuple[tuple[str, ...], ...]] = (
        ("name",),
        ("group_id", "broker_id", "instance_id"),
    )
    INITIAL_DATA: ClassVar[tuple[dict[str, Any], ...]] = (
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
        default=None,
        description="Assigned by generation before the record is considered complete.",
    )
    name: str = Field(description="The account's display name.")
    group_id: int = Field(
        description="Identifies the account group that contains the account."
    )
    broker_id: int = Field(description="Identifies the broker that owns the account.")
    instance_id: int = Field(
        description="Identifies the trading-platform instance used to connect this account."
    )
    base_currency_id: int = Field(
        description="Identifies the base currency used by the account."
    )
    username: str = Field(
        description="The username identifier used to access the trading account."
    )
    password: str = Field(
        repr=False,
        json_schema_extra={"credential": True, "storage_at_rest": "encrypted"},
        description="The credential used to access the trading account.",
    )
    leverage: int = Field(description="Defines the account's leverage multiplier.")
    balance: Decimal = Field(
        default=Decimal(0), description="Stores the account's current balance."
    )
    account_type: str = Field(
        description="Identifies the account model, such as `cfd` or `spread_betting`."
    )
    status: bool = Field(
        default=True, description="Indicates whether the account is active."
    )
    description: str | None = Field(default=None, description="Describes the account.")
