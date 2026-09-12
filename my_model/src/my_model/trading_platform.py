"""The Trading Platform domain entity: a supported trading API standard."""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import Field

from my_model._base import BaseModel


class TradingPlatform(BaseModel):
    """A supported trading API standard, such as MetaTrader 5 or Binance.

    Every trading platform implementation exposes the same
    application-facing trading functions through a dedicated class, keeping
    the system independent of any specific exchange or broker.
    """

    INITIAL_DATA: ClassVar[tuple[dict[str, Any], ...]] = (
        {"name": "MetaTrader 5", "code": "metatrader_5"},
        {"name": "Binance", "code": "binance"},
    )

    id: int | None = Field(
        default=None,
        description="Assigned by generation before the record is considered complete.",
    )
    name: str = Field(description="The platform's display name.")
    code: str = Field(
        description="Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`."
    )
    status: bool = Field(
        default=True, description="Indicates whether the platform is active."
    )
    description: str | None = Field(default=None, description="Describes the platform.")
