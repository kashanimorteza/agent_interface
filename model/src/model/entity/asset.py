"""Asset Entity."""

from model.declaration import Declaration
from model.entity.broker import Broker
from model.foundation import Foundation


class Asset(Foundation, table=True):
    """Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded."""

    id: int | None = Declaration.identity()
    broker_id: int = Declaration.field(
        reference=Broker, description="Identifies the broker that provides this asset."
    )
    symbol: str = Declaration.field(
        description="Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`."
    )
    category: str = Declaration.field(
        description="Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`."
    )
    point_size: float = Declaration.field(
        default=0.0, description="Stores the size of one point for the asset."
    )
    digits: int = Declaration.field(
        default=0,
        description="Stores the number of decimal digits used for the asset's price.",
    )
    is_active: bool = Declaration.field(
        default=True, description="Indicates whether the asset is active."
    )
    description: str | None = Declaration.field(
        nullable=True, description="Describes the asset."
    )

    __table_args__ = Declaration.composite("Asset", unique=(("broker_id", "symbol"),))
