"""The Trading Platform domain entity."""

from __future__ import annotations

from pydantic import Field

from ._base import BaseModel


class TradingPlatform(BaseModel):
    """A supported trading API standard, such as MetaTrader 5 or Binance, kept
    independent of any specific exchange or broker.
    """

    initial_data = (
        {"name": "MetaTrader 5", "code": "metatrader_5"},
        {"name": "Binance", "code": "binance"},
    )

    id: int | None = Field(
        default=None, description="System-generated identity, absent until persisted."
    )
    name: str = Field(min_length=1, description="The platform's display name.")
    code: str = Field(
        min_length=1,
        description="Identifies the implementation class used for this trading platform.",
    )
    status: bool = Field(default=True, description="Whether the platform is active.")
    description: str | None = Field(default=None, description="Describes the platform.")
