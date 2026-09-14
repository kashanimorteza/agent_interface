"""The Account Domain Definition."""

from __future__ import annotations

from decimal import Decimal
from typing import ClassVar

from .foundation import ModelBase, UniqueConstraints, credential_field, identity_field


class Account(ModelBase):
    """A funded trading account through which the system executes trades and launches positions."""

    id: int = identity_field()
    name: str
    group_id: int
    broker_id: int
    instance_id: int
    base_currency_id: int
    username: str
    password: str = credential_field()
    leverage: int
    balance: Decimal = Decimal(0)
    account_type: str
    status: bool = True
    description: str | None = None

    unique_constraints: ClassVar[UniqueConstraints] = (
        ("name",),
        ("group_id", "broker_id", "instance_id"),
    )
