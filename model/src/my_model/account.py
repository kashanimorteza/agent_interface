from __future__ import annotations

from decimal import Decimal
from typing import ClassVar

from pydantic import Field

from ._base import DomainModel
from ._shared import Relationship


class Account(DomainModel):
    name: str = Field(..., description="The account's display name.")
    group_id: int = Field(..., description="Identifies the account group that contains the account.")
    broker_id: int = Field(..., description="Identifies the broker that owns the account.")
    instance_id: int = Field(
        ..., description="Identifies the trading-platform instance used to connect this account."
    )
    base_currency_id: int = Field(..., description="Identifies the base currency used by the account.")
    username: str = Field(..., description="The username identifier used to access the trading account.")
    password: str = Field(..., description="The credential used to access the trading account.")
    leverage: int = Field(..., description="Defines the account's leverage multiplier.")
    balance: Decimal = Field(default=Decimal("0"), description="Stores the account's current balance.")
    account_type: str = Field(
        ..., description="Identifies the account model, such as cfd or spread_betting."
    )
    status: bool = Field(default=True, description="Indicates whether the account is active.")
    description: str | None = Field(default=None, description="Describes the account.")

    unique_fields: ClassVar[frozenset[str]] = frozenset({"name"})
    unique_together: ClassVar[list[tuple[str, ...]]] = [("group_id", "broker_id", "instance_id")]
    credential_fields: ClassVar[frozenset[str]] = frozenset({"password"})
    credential_storage: ClassVar[dict[str, str]] = {"password": "encrypted"}
    relationships: ClassVar[dict[str, Relationship]] = {
        "account_group": Relationship(target="AccountGroup", cardinality="one", field="group_id"),
        "broker": Relationship(target="Broker", cardinality="one", field="broker_id"),
        "instance": Relationship(target="Instance", cardinality="one", field="instance_id"),
        "base_currency": Relationship(target="Currency", cardinality="one", field="base_currency_id"),
    }
    domain_rules: ClassVar[list[str]] = [
        "Instance credentials authenticate the technical Trading Platform connection; Account "
        "credentials authenticate this specific trading account. The same credential must not be "
        "duplicated across both Models unless the selected Trading Platform explicitly requires "
        "it in both roles.",
    ]


ACCOUNT_INITIAL_DATA: list[dict] = [
    {
        "name": "Acc-1",
        "group_id": 1,
        "broker_id": 1,
        "instance_id": 1,
        "base_currency_id": 1,
        "username": "test",
        "password": "<generate securely>",
        "leverage": 100,
        "account_type": "CFD",
    },
]
