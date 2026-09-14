"""The Asset Domain Definition."""

from __future__ import annotations

from pydantic import Field

from .foundation import ModelBase


class Asset(ModelBase):
    """An asset that can be selected for trading, provided by one Broker."""

    UNIQUE_CONSTRAINTS = (("broker_id", "symbol"),)

    id: int | None = Field(default=None, description="Auto-incrementing primary key.")
    broker_id: int = Field(..., description="Identifies the broker that provides this asset.")
    symbol: str = Field(
        ...,
        description="Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`.",
    )
    category: str = Field(
        ...,
        description="Identifies the asset category, such as `Currency`, `Commodity`, "
        "or `Cryptocurrency`.",
    )
    point_size: float = Field(
        default=0.0, description="Stores the size of one point for the asset."
    )
    digits: int = Field(
        default=0, description="Stores the number of decimal digits used for the asset's price."
    )
    is_active: bool = Field(default=True, description="Whether the asset is active.")
    description: str | None = Field(default=None, description="Describes the asset.")
