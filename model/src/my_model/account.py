"""The Account Model."""

from decimal import Decimal
from pydantic import Field

from ._base import Model


class Account(Model):
    """Defines a funded trading account through which the system executes trades and launches
    positions. Each account identifies its broker, account model, and login credentials so the
    system knows where the trade must be sent, how it must connect, and which account must be used
    for the operation.
    """

    id: int | None = Field(default=None, description="Assigned by persistence on create; absent until then.")
    name: str = Field(description="The account's display name. Unique.")
    group_id: int = Field(description="Identifies the account group that contains the account.")
    broker_id: int = Field(description="Identifies the broker that owns the account.")
    base_currency_id: int = Field(description="Identifies the base currency used by the account.")
    username: str = Field(description="The username identifier used to access the trading account.")
    password: str | None = Field(
        default=None,
        description="The credential used to access the trading account. Credential: accepted on write, never returned.",
    )
    leverage: int = Field(description="Defines the account's leverage multiplier.")
    balance: Decimal = Field(default=Decimal("0"), description="Stores the account's current balance.")
    account_type: str = Field(description="Identifies the account model, such as cfd or spread_betting.")
    status: bool = Field(default=True, description="Indicates whether the account is active.")
    description: str | None = Field(default=None, description="Describes the account.")
