"""Trading Platform Domain Definition.

Represents a supported trading API standard, such as MetaTrader 5 or
Binance, independent of any specific exchange or broker.
"""

from __future__ import annotations

from pydantic import Field

from model.foundation import DomainModel


class TradingPlatform(DomainModel):
    """A supported trading platform standard."""

    persistent = True
    unique_sets = (("name",),)

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
    code: str = Field(
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
