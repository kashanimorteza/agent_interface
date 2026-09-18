"""The Account Domain Definition: a funded trading account through which the system executes trades."""

from decimal import Decimal
from typing import ClassVar

from model.foundation import DomainModel, domain_field


class Account(DomainModel):
    """A funded trading account. Its selected Instance owns the separate technical connection
    to the Trading Platform; Account credentials authenticate this specific trading account.
    """

    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (
        ("group_id", "broker_id", "instance_id"),
    )

    id: int | None = domain_field(
        default=None,
        primary_key=True,
        auto_increment=True,
        nullable=False,
        description="Identifies the account.",
    )
    name: str = domain_field(unique=True, description="The account's display name.")
    group_id: int = domain_field(
        foreign_key="AccountGroup.id",
        cardinality="many_to_one",
        description="Identifies the account group that contains the account.",
    )
    broker_id: int = domain_field(
        foreign_key="Broker.id",
        cardinality="many_to_one",
        description="Identifies the broker that owns the account.",
    )
    instance_id: int = domain_field(
        foreign_key="Instance.id",
        cardinality="many_to_one",
        description="Identifies the trading-platform instance used to connect this account.",
    )
    base_currency_id: int = domain_field(
        foreign_key="Currency.id",
        cardinality="many_to_one",
        description="Identifies the base currency used by the account.",
    )
    username: str = domain_field(
        description="The username identifier used to access the trading account."
    )
    password: str = domain_field(
        credential="encrypted",
        description="The credential used to access the trading account.",
    )
    leverage: int = domain_field(
        description="Defines the account's leverage multiplier."
    )
    balance: Decimal = domain_field(
        default=Decimal(0), description="Stores the account's current balance."
    )
    account_type: str = domain_field(
        description="Identifies the account model, such as cfd or spread_betting."
    )
    is_active: bool = domain_field(
        default=True, description="Indicates whether the account is active."
    )
    description: str | None = domain_field(
        default=None, description="Describes the account."
    )
