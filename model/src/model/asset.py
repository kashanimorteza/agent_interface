"""The Asset Domain Definition (Target: Model > Asset)."""

from __future__ import annotations

import pydantic

from model.foundation import (
    ModelFoundation,
    description_field,
    id_field,
    is_active_field,
)


class Asset(ModelFoundation):
    """An asset that can be selected for trading, identifying the complete set of available
    tradable assets and the category of each so the system knows exactly what is being traded."""

    id: int = id_field()
    broker_id: int = pydantic.Field(
        description="Identifies the broker that provides this asset."
    )
    symbol: str = pydantic.Field(
        description="Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`."
    )
    category: str = pydantic.Field(
        description="Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`."
    )
    point_size: float = pydantic.Field(
        default=0.0, description="Stores the size of one point for the asset."
    )
    digits: int = pydantic.Field(
        default=0,
        description="Stores the number of decimal digits used for the asset's price.",
    )
    is_active: bool = is_active_field("Indicates whether the asset is active.")
    description: str | None = description_field("Describes the asset.")
