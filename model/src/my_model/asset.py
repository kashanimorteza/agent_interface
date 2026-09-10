from __future__ import annotations

from typing import ClassVar

from pydantic import Field

from ._base import DomainModel
from ._shared import Relationship


class Asset(DomainModel):
    broker_id: int = Field(..., description="Identifies the broker that provides this asset.")
    symbol: str = Field(
        ..., description="Identifies the tradable asset, such as EUR/USD, XAU/USD, or USOil."
    )
    category: str = Field(
        ..., description="Identifies the asset category, such as Currency, Commodity, or Cryptocurrency."
    )
    point_size: float = Field(default=0.0, description="Stores the size of one point for the asset.")
    digits: int = Field(
        default=0, description="Stores the number of decimal digits used for the asset's price."
    )
    status: bool = Field(default=True, description="Indicates whether the asset is active.")
    description: str | None = Field(default=None, description="Describes the asset.")

    unique_together: ClassVar[list[tuple[str, ...]]] = [("broker_id", "symbol")]
    relationships: ClassVar[dict[str, Relationship]] = {
        "broker": Relationship(target="Broker", cardinality="one", field="broker_id"),
    }


ASSET_INITIAL_DATA: list[dict] = [
    {"broker_id": 1, "symbol": "EUR/USD", "category": "Currency", "point_size": 0.0001, "digits": 5},
    {"broker_id": 1, "symbol": "EUR/GBP", "category": "Currency", "point_size": 0.001, "digits": 5},
    {"broker_id": 1, "symbol": "XAU/USD", "category": "Commodity", "point_size": 0.01, "digits": 2},
    {"broker_id": 1, "symbol": "USOil", "category": "Commodity", "point_size": 0.01, "digits": 3},
]
