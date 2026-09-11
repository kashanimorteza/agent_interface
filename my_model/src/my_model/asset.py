from pydantic import Field

from ._base import BaseModel


class Asset(BaseModel):
    """An asset that can be selected for trading, provided by a Broker."""

    id: int | None = Field(
        default=None, description="Generated once the Asset is persisted."
    )
    broker_id: int = Field(
        description="Identifies the broker that provides this asset."
    )
    symbol: str = Field(description="Identifies the tradable asset.")
    category: str = Field(description="Identifies the asset category.")
    point_size: float = Field(
        default=0.0, description="The size of one point for the asset."
    )
    digits: int = Field(
        default=0,
        description="The number of decimal digits used for the asset's price.",
    )
    status: bool = Field(
        default=True, description="Indicates whether the asset is active."
    )
    description: str | None = Field(default=None, description="Describes the asset.")
