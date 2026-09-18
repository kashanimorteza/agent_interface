"""The Asset Domain Definition: an asset selectable for trading, with its category and price-precision metadata."""

from __future__ import annotations

from typing import ClassVar

from model.foundation import DomainModel, ForeignKeyDeclaration, domain_field


class Asset(DomainModel):
    persistent = True
    unique_sets: ClassVar[list[list[str]]] = [["broker_id", "symbol"]]

    id: int | None = domain_field(
        type="integer", nullable=False, primary_key=True, auto_increment=True
    )
    broker_id: int = domain_field(
        type="integer",
        nullable=False,
        foreign_key=ForeignKeyDeclaration(
            references="Broker", field="id", cardinality="many_to_one", optional=False
        ),
        description="Identifies the broker that provides this asset.",
    )
    symbol: str = domain_field(
        type="string",
        nullable=False,
        description="Identifies the tradable asset, such as EUR/USD, XAU/USD, or USOil.",
    )
    category: str = domain_field(
        type="string",
        nullable=False,
        description="Identifies the asset category, such as Currency, Commodity, or Cryptocurrency.",
    )
    point_size: float = domain_field(
        type="float",
        nullable=False,
        default=0.0,
        description="Stores the size of one point for the asset.",
    )
    digits: int = domain_field(
        type="integer",
        nullable=False,
        default=0,
        description="Stores the number of decimal digits used for the asset's price.",
    )
    is_active: bool = domain_field(
        type="boolean",
        nullable=False,
        default=True,
        description="Indicates whether the asset is active.",
    )
    description: str | None = domain_field(
        type="string", nullable=True, description="Describes the asset."
    )
