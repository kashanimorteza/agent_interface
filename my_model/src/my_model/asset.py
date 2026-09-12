"""The Asset domain entity."""

from __future__ import annotations

from pydantic import Field

from ._base import BaseModel


class Asset(BaseModel):
    """An asset that can be selected for trading, identifying its broker and
    category so the system knows exactly what is being traded.
    """

    initial_data = (
        {
            "broker_id": 1,
            "symbol": "EUR/USD",
            "category": "Currency",
            "point_size": 0.0001,
            "digits": 5,
        },
        {
            "broker_id": 1,
            "symbol": "EUR/GBP",
            "category": "Currency",
            "point_size": 0.001,
            "digits": 5,
        },
        {
            "broker_id": 1,
            "symbol": "XAU/USD",
            "category": "Commodity",
            "point_size": 0.01,
            "digits": 2,
        },
        {
            "broker_id": 1,
            "symbol": "USOil",
            "category": "Commodity",
            "point_size": 0.01,
            "digits": 3,
        },
    )

    id: int | None = Field(
        default=None, description="System-generated identity, absent until persisted."
    )
    broker_id: int = Field(description="Identifies the broker that provides this asset.")
    symbol: str = Field(min_length=1, description="Identifies the tradable asset, such as EUR/USD.")
    category: str = Field(
        min_length=1, description="The asset category, such as Currency or Commodity."
    )
    point_size: float = Field(default=0.0, ge=0, description="The size of one point for the asset.")
    digits: int = Field(default=0, ge=0, description="Decimal digits used for the asset's price.")
    status: bool = Field(default=True, description="Whether the asset is active.")
    description: str | None = Field(default=None, description="Describes the asset.")
