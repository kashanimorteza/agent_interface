"""The Trading Platform Domain Definition."""

from __future__ import annotations

from model.foundation import ModelBase, persistence_field


class TradingPlatform(ModelBase):
    """A supported trading API standard, such as MetaTrader 5 or Binance.

    Keeps the system independent of any specific exchange or broker. Every
    trading platform implementation exposes the same application-facing
    trading functions while handling communication with its destination API
    according to that platform's own mechanism.
    """

    id: int = persistence_field(
        primary_key=True,
        auto_increment=True,
        description="Primary identity of the trading platform.",
    )
    name: str = persistence_field(
        unique=True, description="The platform's display name."
    )
    code: str = persistence_field(
        description="Identifies the implementation class the application must use for this trading platform."
    )
    is_active: bool = persistence_field(
        default=True, description="Indicates whether the platform is active."
    )
    description: str | None = persistence_field(
        default=None, description="Describes the platform."
    )
