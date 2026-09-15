"""The Account Domain Definition."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from model.foundation import DomainModel, field_meta


class Account(DomainModel):
    """A funded trading account through which the system executes trades."""

    __persistent__ = True
    __unique_sets__ = (("group_id", "broker_id", "instance_id"),)

    id: int = Field(json_schema_extra=field_meta(primary_key=True, auto_increment=True))
    name: str = Field(json_schema_extra=field_meta(unique=True))
    group_id: int = Field(
        json_schema_extra=field_meta(
            foreign_key="account_group.id", cardinality="many_to_one"
        )
    )
    broker_id: int = Field(
        json_schema_extra=field_meta(foreign_key="broker.id", cardinality="many_to_one")
    )
    instance_id: int = Field(
        json_schema_extra=field_meta(
            foreign_key="instance.id", cardinality="many_to_one"
        )
    )
    base_currency_id: int = Field(
        json_schema_extra=field_meta(
            foreign_key="currency.id", cardinality="many_to_one"
        )
    )
    username: str = Field(json_schema_extra=field_meta())
    password: str = Field(json_schema_extra=field_meta(credential="encrypted"))
    leverage: int = Field(json_schema_extra=field_meta())
    balance: Decimal = Field(default=Decimal(0), json_schema_extra=field_meta())
    account_type: str = Field(json_schema_extra=field_meta())
    is_active: bool = Field(default=True, json_schema_extra=field_meta())
    description: str | None = Field(
        default=None, json_schema_extra=field_meta(nullable=True)
    )
