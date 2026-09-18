"""Position Domain Definition.

Stores the complete information for every position created by the system,
allowing it to identify and track positions that have been opened as well
as positions that are still pending execution.
"""

from __future__ import annotations

from decimal import Decimal

from pydantic import AwareDatetime, Field

from model.foundation import DomainModel


class Position(DomainModel):
    """One trading position, opened or pending execution."""

    persistent = True
    unique_sets = ()

    id: int | None = Field(
        default=None,
        json_schema_extra={
            "type": "integer",
            "primary_key": True,
            "auto_increment": True,
            "nullable": False,
        },
    )
    user_id: int = Field(
        json_schema_extra={
            "type": "integer",
            "nullable": False,
            "foreign_key": {"references": "User", "field": "id"},
            "cardinality": {
                "of": "Position",
                "to": "User",
                "multiplicity": "many-to-one",
                "optional": False,
            },
        },
    )
    name: str = Field(
        json_schema_extra={"type": "string", "nullable": False, "unique": True},
    )
    trading_platform_id: int = Field(
        json_schema_extra={
            "type": "integer",
            "nullable": False,
            "foreign_key": {"references": "TradingPlatform", "field": "id"},
            "cardinality": {
                "of": "Position",
                "to": "TradingPlatform",
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
                "of": "Position",
                "to": "Broker",
                "multiplicity": "many-to-one",
                "optional": False,
            },
        },
    )
    account_id: int = Field(
        json_schema_extra={
            "type": "integer",
            "nullable": False,
            "foreign_key": {"references": "Account", "field": "id"},
            "cardinality": {
                "of": "Position",
                "to": "Account",
                "multiplicity": "many-to-one",
                "optional": False,
            },
        },
    )
    trailing_group_id: int = Field(
        json_schema_extra={
            "type": "integer",
            "nullable": False,
            "foreign_key": {"references": "TrailingGroup", "field": "id"},
            "cardinality": {
                "of": "Position",
                "to": "TrailingGroup",
                "multiplicity": "many-to-one",
                "optional": False,
            },
        },
    )
    partial_group_id: int = Field(
        json_schema_extra={
            "type": "integer",
            "nullable": False,
            "foreign_key": {"references": "PartialGroup", "field": "id"},
            "cardinality": {
                "of": "Position",
                "to": "PartialGroup",
                "multiplicity": "many-to-one",
                "optional": False,
            },
        },
    )
    action_group_id: int = Field(
        json_schema_extra={
            "type": "integer",
            "nullable": False,
            "foreign_key": {"references": "ActionGroup", "field": "id"},
            "cardinality": {
                "of": "Position",
                "to": "ActionGroup",
                "multiplicity": "many-to-one",
                "optional": False,
            },
        },
    )
    action_id: int = Field(
        json_schema_extra={
            "type": "integer",
            "nullable": False,
            "foreign_key": {"references": "Action", "field": "id"},
            "cardinality": {
                "of": "Position",
                "to": "Action",
                "multiplicity": "many-to-one",
                "optional": False,
            },
        },
    )
    date: AwareDatetime = Field(
        json_schema_extra={"type": "datetime", "nullable": False},
    )
    volume: Decimal = Field(
        json_schema_extra={"type": "decimal", "nullable": False},
    )
    profit: Decimal = Field(
        default=Decimal(0),
        json_schema_extra={"type": "decimal", "nullable": False, "default": "0"},
    )
    is_executed: bool = Field(
        default=False,
        json_schema_extra={"type": "boolean", "nullable": False, "default": False},
    )
    order_type: str = Field(
        json_schema_extra={"type": "string", "nullable": False},
    )
    base_tp: Decimal = Field(
        json_schema_extra={"type": "decimal", "nullable": False},
    )
    base_sl: Decimal = Field(
        json_schema_extra={"type": "decimal", "nullable": False},
    )
    real_tp: Decimal = Field(
        json_schema_extra={"type": "decimal", "nullable": False},
    )
    real_sl: Decimal = Field(
        json_schema_extra={"type": "decimal", "nullable": False},
    )
    is_active: bool = Field(
        default=True,
        json_schema_extra={"type": "boolean", "nullable": False, "default": True},
    )
    description: str | None = Field(
        default=None,
        json_schema_extra={"type": "string", "nullable": True},
    )
