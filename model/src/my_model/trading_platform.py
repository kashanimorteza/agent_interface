from __future__ import annotations

from pydantic import Field

from ._base import DomainModel


class TradingPlatform(DomainModel):
    name: str = Field(..., description="The platform's display name.")
    code: str = Field(
        ...,
        description="Identifies the implementation class the application must use for this trading platform.",
    )
    status: bool = Field(default=True, description="Indicates whether the platform is active.")
    description: str | None = Field(default=None, description="Describes the platform.")


TRADING_PLATFORM_INITIAL_DATA: list[dict] = [
    {"name": "MetaTrader 5", "code": "metatrader_5"},
    {"name": "Binance", "code": "binance"},
]
