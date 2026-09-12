"""The Account domain entity."""

from decimal import Decimal

from pydantic import Field

from my_model._base import BaseModel, credential_field


class Account(BaseModel):
    """A funded trading account through which the system executes trades and
    launches positions.

    Each Account identifies the trading account and its account-level login
    credentials, while its selected Instance owns the separate technical
    connection to the Trading Platform: the same credential must not be
    duplicated across both unless the selected Trading Platform explicitly
    requires it in both roles.
    """

    id: int = Field(description="The account's logical identity.")
    name: str = Field(description="The account's display name.")
    group_id: int = Field(description="Identifies the account group that contains the account.")
    broker_id: int = Field(description="Identifies the broker that owns the account.")
    instance_id: int = Field(
        description="Identifies the trading-platform instance used to connect this account."
    )
    base_currency_id: int = Field(description="Identifies the base currency used by the account.")
    username: str = Field(description="The username identifier used to access the trading account.")
    password: str = credential_field(
        storage_at_rest="encrypted",
        description="The credential used to access the trading account.",
    )
    leverage: int = Field(description="The account's leverage multiplier.")
    balance: Decimal = Field(default=Decimal(0), description="The account's current balance.")
    account_type: str = Field(description="Identifies the account model.")
    status: bool = Field(default=True, description="Whether the account is active.")
    description: str | None = Field(default=None, description="Describes the account.")


# password is generated securely by Database, recognized from this Model's
# own credential declaration.
INITIAL_DATA: list[dict[str, object]] = [
    {
        "name": "Acc-1",
        "group_id": 1,
        "broker_id": 1,
        "instance_id": 1,
        "base_currency_id": 1,
        "username": "test",
        "leverage": 100,
        "account_type": "CFD",
    },
]
