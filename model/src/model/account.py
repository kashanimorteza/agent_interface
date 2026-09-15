"""Domain Definition for Account."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from model.foundation import Credential, DomainModel, ForeignKey


class Account(DomainModel):
    """Defines a funded trading account through which the system executes trades and
    launches positions.
    """

    __primary_key__ = ("id",)
    __auto_increment__ = ("id",)
    __unique__ = ("name",)
    __unique_sets__ = (("group_id", "broker_id", "instance_id"),)
    __foreign_keys__ = {
        "group_id": ForeignKey(target="AccountGroup", field="id", cardinality="many_to_one"),
        "broker_id": ForeignKey(target="Broker", field="id", cardinality="many_to_one"),
        "instance_id": ForeignKey(target="Instance", field="id", cardinality="many_to_one"),
        "base_currency_id": ForeignKey(target="Currency", field="id", cardinality="many_to_one"),
    }
    __credentials__ = {"password": Credential.ENCRYPTED}

    id: int = Field(...)
    name: str = Field(...)
    group_id: int = Field(...)
    broker_id: int = Field(...)
    instance_id: int = Field(...)
    base_currency_id: int = Field(...)
    username: str = Field(...)
    password: str = Field(...)
    leverage: int = Field(...)
    balance: Decimal = Field(default=Decimal(0))
    account_type: str = Field(...)
    is_active: bool = Field(default=True)
    description: str | None = Field(default=None)
