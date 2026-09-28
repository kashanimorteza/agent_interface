"""Account Entity."""

from decimal import Decimal

from model.declaration import Declaration, Sensitivity
from model.entity.account_group import AccountGroup
from model.entity.broker import Broker
from model.entity.currency import Currency
from model.entity.instance import Instance
from model.foundation import Foundation


class Account(Foundation, table=True):
    """Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform."""

    id: int | None = Declaration.identity()
    name: str = Declaration.field(
        unique=True, description="The account's display name."
    )
    group_id: int = Declaration.field(
        reference=AccountGroup,
        description="Identifies the account group that contains the account.",
    )
    broker_id: int = Declaration.field(
        reference=Broker, description="Identifies the broker that owns the account."
    )
    instance_id: int = Declaration.field(
        reference=Instance,
        description="Identifies the trading-platform instance used to connect this account.",
    )
    base_currency_id: int = Declaration.field(
        reference=Currency,
        description="Identifies the base currency used by the account.",
    )
    username: str = Declaration.field(
        description="The username identifier used to access the trading account."
    )
    password: str = Declaration.field(
        sensitivity=Sensitivity.PASSWORD,
        description="The credential used to access the trading account.",
    )
    leverage: int = Declaration.field(
        description="Defines the account's leverage multiplier."
    )
    balance: Decimal = Declaration.field(
        default=Decimal(0), description="Stores the account's current balance."
    )
    account_type: str = Declaration.field(
        description="Identifies the account model, such as `cfd` or `spread_betting`."
    )
    is_active: bool = Declaration.field(
        default=True, description="Indicates whether the account is active."
    )
    description: str | None = Declaration.field(
        nullable=True, description="Describes the account."
    )

    __table_args__ = Declaration.composite(
        "Account", unique=(("group_id", "broker_id", "instance_id"),)
    )
