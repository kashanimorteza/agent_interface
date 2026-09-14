"""The Trading Platform Domain Definition."""

from __future__ import annotations

from pydantic import Field

from .foundation import ModelBase


class TradingPlatform(ModelBase):
    """A supported trading API standard, independent of any specific exchange or broker."""

    id: int | None = Field(default=None, description="Auto-incrementing primary key.")
    name: str = Field(..., description="The platform's display name.")
    code: str = Field(
        ...,
        description="Identifies the implementation class the application must use for this "
        "trading platform, such as `binance` or `metatrader_5`.",
    )
    is_active: bool = Field(default=True, description="Whether the platform is active.")
    description: str | None = Field(default=None, description="Describes the platform.")
