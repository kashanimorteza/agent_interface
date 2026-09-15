"""The Asset Domain Definition."""

from __future__ import annotations

from typing import ClassVar

from model.foundation import ModelBase, persistence_field


class Asset(ModelBase):
    """An asset that can be selected for trading, provided by a Broker.

    Provides the system with the complete set of available tradable assets
    and identifies the category of each asset.
    """

    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (("broker_id", "symbol"),)

    id: int = persistence_field(
        primary_key=True,
        auto_increment=True,
        description="Primary identity of the asset.",
    )
    broker_id: int = persistence_field(
        foreign_key="broker.id",
        description="Identifies the broker that provides this asset.",
    )
    symbol: str = persistence_field(
        description="Identifies the tradable asset, such as EUR/USD, XAU/USD, or USOil."
    )
    category: str = persistence_field(
        description="Identifies the asset category, such as Currency, Commodity, or Cryptocurrency."
    )
    point_size: float = persistence_field(
        default=0.0, description="Stores the size of one point for the asset."
    )
    digits: int = persistence_field(
        default=0,
        description="Stores the number of decimal digits used for the asset's price.",
    )
    is_active: bool = persistence_field(
        default=True, description="Indicates whether the asset is active."
    )
    description: str | None = persistence_field(
        default=None, description="Describes the asset."
    )
