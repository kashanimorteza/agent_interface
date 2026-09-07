"""Asset: an asset that can be selected for trading."""

from __future__ import annotations

from .base import Model, field


class Asset(Model):
    """Defines an asset that can be selected for trading. It provides the
    system with the complete set of available tradable assets and identifies
    the category of each asset so the system knows exactly what is being
    traded."""

    id: int | None = field("integer", primary_key=True, auto_increment=True)
    name: str = field("string", unique=True, purpose="The asset's display name.")
    symbol: str = field(
        "string",
        unique=True,
        purpose="Identifies the tradable asset, such as EUR/USD, XAU/USD, or USOil.",
    )
    category: str = field(
        "string",
        purpose="Identifies the asset category, such as Currency, Commodity, or Cryptocurrency.",
    )
    point_size: float = field(
        "float", default=0.0, purpose="Stores the size of one point for the asset."
    )
    digits: int = field(
        "integer",
        default=0,
        purpose="Stores the number of decimal digits used for the asset's price.",
    )
    status: bool = field("boolean", default=True, purpose="Indicates whether the asset is active.")
    description: str | None = field("string", nullable=True, purpose="Describes the asset.")

    initial_data = (
        {"name": "EURUSD", "symbol": "EUR/USD", "category": "Currency", "point_size": 0.0001, "digits": 5},
        {"name": "EURGBP", "symbol": "EUR/GBP", "category": "Currency", "point_size": 0.001, "digits": 5},
        {"name": "XAUUSD", "symbol": "XAU/USD", "category": "Commodity", "point_size": 0.01, "digits": 2},
        {"name": "USOil", "symbol": "USOil", "category": "Commodity", "point_size": 0.01, "digits": 3},
    )
