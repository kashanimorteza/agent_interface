"""The Asset Model."""

from pydantic import Field

from ._base import Model


class Asset(Model):
    """Defines an asset that can be selected for trading. It provides the system with the complete set
    of available tradable assets and identifies the category of each asset so the system knows
    exactly what is being traded.
    """

    id: int | None = Field(default=None, description="Assigned by persistence on create; absent until then.")
    name: str = Field(description="The asset's display name. Unique.")
    symbol: str = Field(description="Identifies the tradable asset, such as EUR/USD, XAU/USD, or USOil. Unique.")
    category: str = Field(
        description="Identifies the asset category, such as Currency, Commodity, or Cryptocurrency.",
    )
    point_size: float = Field(default=0.0, description="Stores the size of one point for the asset.")
    digits: int = Field(default=0, description="Stores the number of decimal digits used for the asset's price.")
    status: bool = Field(default=True, description="Indicates whether the asset is active.")
    description: str | None = Field(default=None, description="Describes the asset.")
