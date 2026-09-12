"""The Asset domain Model: an asset that can be selected for trading."""

from pydantic import Field

from ._base import BaseModel


class Asset(BaseModel):
    """An asset that can be selected for trading.

    Provides the system with the complete set of available tradable assets and
    identifies the category of each asset. The combination-uniqueness of
    `broker_id` and `symbol` is a domain rule traceable to this Model, enforced
    by Database.
    """

    id: int | None = Field(default=None, description="The asset's generated identity.")
    broker_id: int = Field(description="Identifies the broker that provides this asset.")
    symbol: str = Field(
        description="Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`."
    )
    category: str = Field(
        description="Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`."
    )
    point_size: float = Field(default=0.0, description="Stores the size of one point for the asset.")
    digits: int = Field(
        default=0, description="Stores the number of decimal digits used for the asset's price."
    )
    status: bool = Field(default=True, description="Indicates whether the asset is active.")
    description: str | None = Field(default=None, description="Describes the asset.")


INITIAL_DATA: list[dict[str, object]] = [
    {"broker_id": 1, "symbol": "EUR/USD", "category": "Currency", "point_size": 0.0001, "digits": 5},
    {"broker_id": 1, "symbol": "EUR/GBP", "category": "Currency", "point_size": 0.001, "digits": 5},
    {"broker_id": 1, "symbol": "XAU/USD", "category": "Commodity", "point_size": 0.01, "digits": 2},
    {"broker_id": 1, "symbol": "USOil", "category": "Commodity", "point_size": 0.01, "digits": 3},
]
