"""A supported trading API standard, independent of any specific exchange or broker."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from ._base import DomainModel


class TradingPlatform(DomainModel):
    """A trading platform whose implementation class the application selects by code."""

    id: int | None = Field(default=None, description="Primary key, auto-incremented.")
    name: str = Field(description="The platform's display name.")
    code: str = Field(
        description="Identifies the implementation class the application must use for this trading platform."
    )
    status: bool = Field(default=True, description="Indicates whether the platform is active.")
    description: str | None = Field(default=None, description="Describes the platform.")


INITIAL_DATA: tuple[dict[str, Any], ...] = (
    {"name": "MetaTrader 5", "code": "metatrader_5"},
    {"name": "Binance", "code": "binance"},
)
