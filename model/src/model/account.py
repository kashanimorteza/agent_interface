"""The Account Domain Definition."""

from __future__ import annotations

from decimal import Decimal
from typing import ClassVar

from model.foundation import CredentialTreatment, ModelBase, persistence_field


class Account(ModelBase):
    """A funded trading account through which the system executes trades and launches positions.

    Identifies the trading account and its account-level login credentials,
    while its selected Instance owns the separate technical connection to
    the Trading Platform. Instance credentials authenticate the technical
    Trading Platform connection; Account credentials authenticate this
    specific trading account. The same credential is not duplicated across
    both unless the selected Trading Platform explicitly requires it in both
    roles; evaluating that exception needs the referenced Trading Platform's
    own data and is resolved by the Component that carries that
    operation-specific context.
    """

    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (
        ("group_id", "broker_id", "instance_id"),
    )

    id: int = persistence_field(
        primary_key=True,
        auto_increment=True,
        description="Primary identity of the account.",
    )
    name: str = persistence_field(
        unique=True, description="The account's display name."
    )
    group_id: int = persistence_field(
        foreign_key="account_group.id",
        description="Identifies the account group that contains the account.",
    )
    broker_id: int = persistence_field(
        foreign_key="broker.id",
        description="Identifies the broker that owns the account.",
    )
    instance_id: int = persistence_field(
        foreign_key="instance.id",
        description="Identifies the trading-platform instance used to connect this account.",
    )
    base_currency_id: int = persistence_field(
        foreign_key="currency.id",
        description="Identifies the base currency used by the account.",
    )
    username: str = persistence_field(
        description="The username identifier used to access the trading account."
    )
    password: str = persistence_field(
        credential=CredentialTreatment.ENCRYPTED,
        description="The credential used to access the trading account.",
    )
    leverage: int = persistence_field(
        description="Defines the account's leverage multiplier."
    )
    balance: Decimal = persistence_field(
        default=Decimal(0), description="Stores the account's current balance."
    )
    account_type: str = persistence_field(
        description="Identifies the account model, such as cfd or spread_betting."
    )
    is_active: bool = persistence_field(
        default=True, description="Indicates whether the account is active."
    )
    description: str | None = persistence_field(
        default=None, description="Describes the account."
    )
