"""The Account Domain Definition."""

from __future__ import annotations

from decimal import Decimal

from model.foundation import (
    DomainModel,
    FieldContract,
    PersistenceContract,
    RelationshipContract,
)


class Account(DomainModel):
    """A funded trading account through which the system executes trades and
    launches positions.

    Each Account identifies the trading account and its account-level login
    credentials, while its selected Instance owns the separate technical
    connection to the Trading Platform.

    Instance credentials authenticate the technical Trading Platform
    connection; Account credentials authenticate this specific trading
    account. The same credential must not be duplicated across both unless
    the selected Trading Platform explicitly requires it in both roles. That
    cross-Domain-Definition rule is not evaluable from Account data alone
    and is enforced outside Model.
    """

    id: int | None = None
    name: str
    group_id: int
    broker_id: int
    instance_id: int
    base_currency_id: int
    username: str
    password: str
    leverage: int
    balance: Decimal = Decimal(0)
    account_type: str
    is_active: bool = True
    description: str | None = None

    PERSISTENCE_CONTRACT = PersistenceContract(
        persistent=True,
        fields={
            "id": FieldContract(primary_key=True, auto_increment=True, nullable=False),
            "name": FieldContract(unique=True, nullable=False),
            "group_id": FieldContract(nullable=False),
            "broker_id": FieldContract(nullable=False),
            "instance_id": FieldContract(nullable=False),
            "base_currency_id": FieldContract(nullable=False),
            "username": FieldContract(nullable=False),
            "password": FieldContract(nullable=False, credential="encrypted"),
            "leverage": FieldContract(nullable=False),
            "balance": FieldContract(nullable=False, default=Decimal(0)),
            "account_type": FieldContract(nullable=False),
            "is_active": FieldContract(nullable=False, default=True),
            "description": FieldContract(nullable=True),
        },
        relationships=(
            RelationshipContract(field="group_id", references="AccountGroup"),
            RelationshipContract(field="broker_id", references="Broker"),
            RelationshipContract(field="instance_id", references="Instance"),
            RelationshipContract(field="base_currency_id", references="Currency"),
        ),
        unique_sets=(("group_id", "broker_id", "instance_id"),),
    )
