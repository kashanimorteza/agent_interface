"""Partial Rule Domain Definition.

Represents one individual Partial Close rule that tells the system under
which condition part of an open position must be closed and how much of
its volume must be closed.
"""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from model.foundation import DomainModel


class PartialRule(DomainModel):
    """One activation-and-close-volume rule within a Partial Group."""

    persistent = True
    unique_sets = (("partial_group_id", "profit_percentage"),)

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
    partial_group_id: int = Field(
        json_schema_extra={
            "type": "integer",
            "nullable": False,
            "foreign_key": {"references": "PartialGroup", "field": "id"},
            "cardinality": {
                "of": "PartialRule",
                "to": "PartialGroup",
                "multiplicity": "many-to-one",
                "optional": False,
            },
        },
    )
    profit_percentage: Decimal = Field(
        json_schema_extra={"type": "decimal", "nullable": False},
    )
    close_percentage: Decimal = Field(
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
