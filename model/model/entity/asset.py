"""The Asset Entity."""

from typing import ClassVar

from model.core.declaration import Declaration, FieldDeclaration, Relation
from model.core.foundation import Foundation


class Asset(Foundation):
    declaration: ClassVar[Declaration] = Declaration(
        name="Asset",
        description="Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.",
        fields=(
            FieldDeclaration(
                name="id",
                type="integer",
                nullable=False,
                immutable=True,
                value_generation="auto_increment",
            ),
            FieldDeclaration(
                name="broker_id",
                description="Identifies the broker that provides this asset.",
                type="integer",
                nullable=False,
            ),
            FieldDeclaration(
                name="symbol",
                description="Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`.",
                type="string",
                nullable=False,
            ),
            FieldDeclaration(
                name="category",
                description="Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`.",
                type="string",
                nullable=False,
            ),
            FieldDeclaration(
                name="point_size",
                description="Stores the size of one point for the asset.",
                type="float",
                nullable=False,
                has_default=True,
                default=0.0,
            ),
            FieldDeclaration(
                name="digits",
                description="Stores the number of decimal digits used for the asset's price.",
                type="integer",
                nullable=False,
                has_default=True,
                default=0,
            ),
            FieldDeclaration(
                name="is_active",
                description="Indicates whether the asset is active.",
                type="boolean",
                nullable=False,
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                description="Describes the asset.",
                type="string",
                nullable=True,
            ),
        ),
        primary_key="id",
        relations=(Relation("broker_id", "Broker", "id"),),
        unique_constraints=(("broker_id", "symbol"),),
    )

    id: int | None = None
    broker_id: int
    symbol: str
    category: str
    point_size: float = 0.0
    digits: int = 0
    is_active: bool = True
    description: str | None = None
