"""The Asset Entity."""

from typing import ClassVar

from ..core.base import EntityBase
from ..core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    ValueGeneration,
)


class Asset(EntityBase):
    """The Asset Entity; its Declaration states its complete meaning."""

    declaration: ClassVar[Declaration] = Declaration(
        name="Asset",
        description="Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.",
        fields=(
            FieldDeclaration(
                name="id",
                description=None,
                type=FieldType.INTEGER,
                nullable=False,
                immutable=True,
                value_generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration(
                name="broker_id",
                description="Identifies the broker that provides this asset.",
                type=FieldType.INTEGER,
                nullable=False,
            ),
            FieldDeclaration(
                name="symbol",
                description="Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`.",
                type=FieldType.STRING,
                nullable=False,
            ),
            FieldDeclaration(
                name="category",
                description="Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`.",
                type=FieldType.STRING,
                nullable=False,
            ),
            FieldDeclaration(
                name="point_size",
                description="Stores the size of one point for the asset.",
                type=FieldType.FLOAT,
                nullable=False,
                has_default=True,
                default=0.0,
            ),
            FieldDeclaration(
                name="digits",
                description="Stores the number of decimal digits used for the asset's price.",
                type=FieldType.INTEGER,
                nullable=False,
                has_default=True,
                default=0,
            ),
            FieldDeclaration(
                name="is_active",
                description="Indicates whether the asset is active.",
                type=FieldType.BOOLEAN,
                nullable=False,
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                description="Describes the asset.",
                type=FieldType.STRING,
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
