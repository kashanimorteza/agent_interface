"""The Account Domain Definition: a funded trading account through which the system executes trades and launches positions."""

from __future__ import annotations

from decimal import Decimal
from typing import ClassVar

from model.foundation import (
    CredentialDeclaration,
    DomainModel,
    ForeignKeyDeclaration,
    domain_field,
)


class Account(DomainModel):
    persistent = True
    unique_sets: ClassVar[list[list[str]]] = [["group_id", "broker_id", "instance_id"]]

    id: int | None = domain_field(
        type="integer", nullable=False, primary_key=True, auto_increment=True
    )
    name: str = domain_field(
        type="string",
        nullable=False,
        unique=True,
        description="The account's display name.",
    )
    group_id: int = domain_field(
        type="integer",
        nullable=False,
        foreign_key=ForeignKeyDeclaration(
            references="AccountGroup",
            field="id",
            cardinality="many_to_one",
            optional=False,
        ),
        description="Identifies the account group that contains the account.",
    )
    broker_id: int = domain_field(
        type="integer",
        nullable=False,
        foreign_key=ForeignKeyDeclaration(
            references="Broker", field="id", cardinality="many_to_one", optional=False
        ),
        description="Identifies the broker that owns the account.",
    )
    instance_id: int = domain_field(
        type="integer",
        nullable=False,
        foreign_key=ForeignKeyDeclaration(
            references="Instance", field="id", cardinality="many_to_one", optional=False
        ),
        description="Identifies the trading-platform instance used to connect this account.",
    )
    base_currency_id: int = domain_field(
        type="integer",
        nullable=False,
        foreign_key=ForeignKeyDeclaration(
            references="Currency", field="id", cardinality="many_to_one", optional=False
        ),
        description="Identifies the base currency used by the account.",
    )
    username: str = domain_field(
        type="string",
        nullable=False,
        description="The username identifier used to access the trading account.",
    )
    password: str = domain_field(
        type="string",
        nullable=False,
        credential=CredentialDeclaration(
            classification="credential", treatment="encrypted"
        ),
        description="The credential used to access the trading account.",
    )
    leverage: int = domain_field(
        type="integer",
        nullable=False,
        description="Defines the account's leverage multiplier.",
    )
    balance: Decimal = domain_field(
        type="decimal",
        nullable=False,
        default=Decimal(0),
        description="Stores the account's current balance.",
    )
    account_type: str = domain_field(
        type="string",
        nullable=False,
        description="Identifies the account model, such as cfd or spread_betting.",
    )
    is_active: bool = domain_field(
        type="boolean",
        nullable=False,
        default=True,
        description="Indicates whether the account is active.",
    )
    description: str | None = domain_field(
        type="string", nullable=True, description="Describes the account."
    )
