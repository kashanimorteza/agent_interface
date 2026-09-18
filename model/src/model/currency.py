"""Currency Domain Definition.

Represents a currency usable by the trading system, owned by one User, and
identifies its standard code, display symbol, associated country or
region, and monetary decimal precision.
"""

from __future__ import annotations

from pydantic import Field

from model.foundation import DomainModel


class Currency(DomainModel):
    """A currency owned by one User."""

    persistent = True
    unique_sets = (("user_id", "code"),)

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
                "of": "Currency",
                "to": "User",
                "multiplicity": "many-to-one",
                "optional": False,
            },
        },
    )
    code: str = Field(
        max_length=3,
        json_schema_extra={"type": "string", "length": 3, "nullable": False},
    )
    symbol: str | None = Field(
        default=None,
        json_schema_extra={"type": "string", "nullable": True},
    )
    country: str | None = Field(
        default=None,
        json_schema_extra={"type": "string", "nullable": True},
    )
    decimal_digits: int = Field(
        default=2,
        json_schema_extra={"type": "integer", "nullable": False, "default": 2},
    )
    is_active: bool = Field(
        default=True,
        json_schema_extra={"type": "boolean", "nullable": False, "default": True},
    )
    description: str | None = Field(
        default=None,
        json_schema_extra={"type": "string", "nullable": True},
    )
