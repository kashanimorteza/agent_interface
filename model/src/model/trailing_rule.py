"""Trailing Rule Domain Definition.

Represents one individual rule within a Trailing Group that tells the
system when and how to manage Take Profit and Stop Loss.
"""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from model.foundation import DomainModel


class TrailingRule(DomainModel):
    """One activation-and-adjustment rule within a Trailing Group."""

    persistent = True
    unique_sets = (("trailing_group_id", "trigger_percentage"),)

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
    trailing_group_id: int = Field(
        json_schema_extra={
            "type": "integer",
            "nullable": False,
            "foreign_key": {"references": "TrailingGroup", "field": "id"},
            "cardinality": {
                "of": "TrailingRule",
                "to": "TrailingGroup",
                "multiplicity": "many-to-one",
                "optional": False,
            },
        },
    )
    trigger_percentage: Decimal = Field(
        json_schema_extra={"type": "decimal", "nullable": False},
    )
    take_profit_adjustment: Decimal | None = Field(
        default=None,
        json_schema_extra={"type": "decimal", "nullable": True},
    )
    stop_loss_adjustment: Decimal | None = Field(
        default=None,
        json_schema_extra={"type": "decimal", "nullable": True},
    )
    is_active: bool = Field(
        default=True,
        json_schema_extra={"type": "boolean", "nullable": False, "default": True},
    )
    description: str | None = Field(
        default=None,
        json_schema_extra={"type": "string", "nullable": True},
    )
