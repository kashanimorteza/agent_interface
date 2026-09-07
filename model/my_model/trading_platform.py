"""Trading Platform: a supported trading API standard."""

from __future__ import annotations

from .base import Model, field


class TradingPlatform(Model):
    """Defines a supported trading API standard, such as MetaTrader 5 or
    Binance, while keeping the system independent of any specific exchange or
    broker. Every trading platform implementation exposes the same
    application-facing trading functions through a dedicated class, while
    handling communication with its destination API according to that
    platform's own mechanism. Additional platform implementations can be added
    without changing the system's common trading interface."""

    logical_name = "Trading Platform"

    id: int | None = field("integer", primary_key=True, auto_increment=True)
    name: str = field("string", unique=True, purpose="The platform's display name.")
    code: str = field(
        "string",
        purpose="Identifies the implementation class the application must use for this trading platform, such as binance or metatrader_5.",
    )
    status: bool = field("boolean", default=True, purpose="Indicates whether the platform is active.")
    description: str | None = field("string", nullable=True, purpose="Describes the platform.")

    initial_data = (
        {"name": "MetaTrader 5", "code": "metatrader_5"},
        {"name": "Binance", "code": "binance"},
    )
