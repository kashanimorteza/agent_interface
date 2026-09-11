from decimal import Decimal

from pydantic import Field

from ._base import BaseModel


class Account(BaseModel):
    """A funded trading account through which the system executes trades and launches positions."""

    id: int | None = Field(
        default=None, description="Generated once the Account is persisted."
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
        description="The credential used to access the trading account.",
        json_schema_extra={"credential": True},
    )
    leverage: int = Field(description="The account's leverage multiplier.")
    balance: Decimal = Field(
        default=Decimal(0), description="The account's current balance."
    )
    account_type: str = Field(
        description="Identifies the account model, such as cfd or spread_betting."
    )
    status: bool = Field(
        default=True, description="Indicates whether the account is active."
    )
    description: str | None = Field(default=None, description="Describes the account.")
