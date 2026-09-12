"""The Asset domain entity."""

from pydantic import Field

from my_model._base import BaseModel


class Asset(BaseModel):
    """An asset that can be selected for trading, identifying the complete
    set of available tradable assets and each asset's category.
    """

    id: int = Field(description="The asset's logical identity.")
    broker_id: int = Field(description="Identifies the broker that provides this asset.")
    symbol: str = Field(description="Identifies the tradable asset.")
    category: str = Field(description="Identifies the asset category.")
    point_size: float = Field(default=0.0, description="The size of one point for the asset.")
    digits: int = Field(
        default=0, description="The number of decimal digits used for the asset's price."
    )
    status: bool = Field(default=True, description="Whether the asset is active.")
    description: str | None = Field(default=None, description="Describes the asset.")


INITIAL_DATA: list[dict[str, object]] = [
    {"broker_id": 1, "symbol": "EUR/USD", "category": "Currency", "point_size": 0.0001, "digits": 5},
    {"broker_id": 1, "symbol": "EUR/GBP", "category": "Currency", "point_size": 0.001, "digits": 5},
    {"broker_id": 1, "symbol": "XAU/USD", "category": "Commodity", "point_size": 0.01, "digits": 2},
    {"broker_id": 1, "symbol": "USOil", "category": "Commodity", "point_size": 0.01, "digits": 3},
]
