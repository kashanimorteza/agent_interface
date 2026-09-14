"""The Trading Platform Domain Definition (Target: Model > Trading Platform)."""

from __future__ import annotations

import pydantic

from model.foundation import (
    ModelFoundation,
    description_field,
    id_field,
    is_active_field,
)


class TradingPlatform(ModelFoundation):
    """A supported trading API standard, such as MetaTrader 5 or Binance, kept independent of
    any specific exchange or broker."""

    id: int = id_field()
    name: str = pydantic.Field(description="The platform's display name.")
    code: str = pydantic.Field(
        description="Identifies the implementation class the application must use for this "
        "trading platform, such as `binance` or `metatrader_5`."
    )
    is_active: bool = is_active_field("Indicates whether the platform is active.")
    description: str | None = description_field("Describes the platform.")
