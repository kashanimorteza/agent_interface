"""The Account Domain Definition."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from .foundation import ModelBase


class Account(ModelBase):
    """A funded trading account through which the system executes trades and launches positions."""

    UNIQUE_CONSTRAINTS = (
        ("name",),
        ("group_id", "broker_id", "instance_id"),
    )

    id: int | None = Field(default=None, description="Auto-incrementing primary key.")
    name: str = Field(..., description="The account's display name.")
    group_id: int = Field(
        ..., description="Identifies the account group that contains the account."
    )
    broker_id: int = Field(..., description="Identifies the broker that owns the account.")
    instance_id: int = Field(
        ..., description="Identifies the trading-platform instance used to connect this account."
    )
    base_currency_id: int = Field(
        ..., description="Identifies the base currency used by the account."
    )
    username: str = Field(
        ..., description="The username identifier used to access the trading account."
    )
    password: str = Field(
        ...,
        json_schema_extra={"credential": True},
        description="The credential used to access the trading account.",
    )
    leverage: int = Field(..., description="Defines the account's leverage multiplier.")
    balance: Decimal = Field(
        default=Decimal("0"), description="Stores the account's current balance."
    )
    account_type: str = Field(
        ..., description="Identifies the account model, such as `cfd` or `spread_betting`."
    )
    is_active: bool = Field(default=True, description="Whether the account is active.")
    description: str | None = Field(default=None, description="Describes the account.")
