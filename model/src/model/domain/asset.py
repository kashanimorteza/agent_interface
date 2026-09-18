"""The Asset Domain Definition: a tradable asset provided by a Broker."""

from typing import ClassVar

from model.foundation import DomainModel, domain_field


class Asset(DomainModel):
    """A tradable asset, identifying its category so the system knows exactly what is being traded."""

    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (("broker_id", "symbol"),)

    id: int | None = domain_field(
        default=None,
        primary_key=True,
        auto_increment=True,
        nullable=False,
        description="Identifies the asset.",
    )
    broker_id: int = domain_field(
        foreign_key="Broker.id",
        cardinality="many_to_one",
        description="Identifies the broker that provides this asset.",
    )
    symbol: str = domain_field(
        description="Identifies the tradable asset, such as EUR/USD, XAU/USD, or USOil."
    )
    category: str = domain_field(
        description="Identifies the asset category, such as Currency, Commodity, or Cryptocurrency."
    )
    point_size: float = domain_field(
        default=0.0, description="Stores the size of one point for the asset."
    )
    digits: int = domain_field(
        default=0,
        description="Stores the number of decimal digits used for the asset's price.",
    )
    is_active: bool = domain_field(
        default=True, description="Indicates whether the asset is active."
    )
    description: str | None = domain_field(
        default=None, description="Describes the asset."
    )
