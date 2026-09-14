"""The Account Domain Definition (Target: Model > Account)."""

from __future__ import annotations

import decimal
from typing import ClassVar

import pydantic

from model.foundation import (
    ExactDecimal,
    ModelFoundation,
    description_field,
    id_field,
    is_active_field,
)


class Account(ModelFoundation):
    """A funded trading account through which the system executes trades and launches
    positions. Each Account identifies the trading account and its account-level login
    credentials, while its selected Instance owns the separate technical connection to the
    Trading Platform."""

    CREDENTIAL_STORAGE: ClassVar[dict[str, str]] = {"password": "encrypted"}

    id: int = id_field()
    name: str = pydantic.Field(description="The account's display name.")
    group_id: int = pydantic.Field(
        description="Identifies the account group that contains the account."
    )
    broker_id: int = pydantic.Field(
        description="Identifies the broker that owns the account."
    )
    instance_id: int = pydantic.Field(
        description="Identifies the trading-platform instance used to connect this account."
    )
    base_currency_id: int = pydantic.Field(
        description="Identifies the base currency used by the account."
    )
    username: str = pydantic.Field(
        description="The username identifier used to access the trading account."
    )
    password: str = pydantic.Field(
        description="The credential used to access the trading account."
    )
    leverage: int = pydantic.Field(
        description="Defines the account's leverage multiplier."
    )
    balance: ExactDecimal = pydantic.Field(
        default=decimal.Decimal(0), description="Stores the account's current balance."
    )
    account_type: str = pydantic.Field(
        description="Identifies the account model, such as `cfd` or `spread_betting`."
    )
    is_active: bool = is_active_field("Indicates whether the account is active.")
    description: str | None = description_field("Describes the account.")
