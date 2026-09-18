"""Account Domain Definition.

Represents a funded trading account through which the system executes
trades and launches positions. Account credentials authenticate this
specific trading account, separate from the technical Trading Platform
connection credentials owned by its Instance.
"""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from model.foundation import DomainModel


class Account(DomainModel):
    """A funded trading account."""

    persistent = True
    unique_sets = (("group_id", "broker_id", "instance_id"),)

    id: int | None = Field(
        default=None,
        json_schema_extra={
            "type": "integer",
            "primary_key": True,
            "auto_increment": True,
            "nullable": False,
        },
    )
    name: str = Field(
        json_schema_extra={"type": "string", "nullable": False, "unique": True},
    )
    group_id: int = Field(
        json_schema_extra={
            "type": "integer",
            "nullable": False,
            "foreign_key": {"references": "AccountGroup", "field": "id"},
            "cardinality": {
                "of": "Account",
                "to": "AccountGroup",
                "multiplicity": "many-to-one",
                "optional": False,
            },
        },
    )
    broker_id: int = Field(
        json_schema_extra={
            "type": "integer",
            "nullable": False,
            "foreign_key": {"references": "Broker", "field": "id"},
            "cardinality": {
                "of": "Account",
                "to": "Broker",
                "multiplicity": "many-to-one",
                "optional": False,
            },
        },
    )
    instance_id: int = Field(
        json_schema_extra={
            "type": "integer",
            "nullable": False,
            "foreign_key": {"references": "Instance", "field": "id"},
            "cardinality": {
                "of": "Account",
                "to": "Instance",
                "multiplicity": "many-to-one",
                "optional": False,
            },
        },
    )
    base_currency_id: int = Field(
        json_schema_extra={
            "type": "integer",
            "nullable": False,
            "foreign_key": {"references": "Currency", "field": "id"},
            "cardinality": {
                "of": "Account",
                "to": "Currency",
                "multiplicity": "many-to-one",
                "optional": False,
            },
        },
    )
    username: str = Field(
        json_schema_extra={"type": "string", "nullable": False},
    )
    password: str = Field(
        json_schema_extra={
            "type": "string",
            "nullable": False,
            "credential": "encrypted",
        },
    )
    leverage: int = Field(
        json_schema_extra={"type": "integer", "nullable": False},
    )
    balance: Decimal = Field(
        default=Decimal(0),
        json_schema_extra={"type": "decimal", "nullable": False, "default": "0"},
    )
    account_type: str = Field(
        json_schema_extra={"type": "string", "nullable": False},
    )
    is_active: bool = Field(
        default=True,
        json_schema_extra={"type": "boolean", "nullable": False, "default": True},
    )
    description: str | None = Field(
        default=None,
        json_schema_extra={"type": "string", "nullable": True},
    )
