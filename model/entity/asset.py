from typing import ClassVar

from sqlmodel import Field

from ..core.base import Entity
from ..core.declaration import Declaration, FieldDeclaration, Relation, ValueGeneration
from ..core.logical_type import Float, LogicalType


class Asset(Entity, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="Asset",
        description="Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.",
        fields=(
            FieldDeclaration(
                name="id",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=False,
                default=None,
                immutable=True,
                value_generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration(
                name="broker_id",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Identifies the broker that provides this asset.",
            ),
            FieldDeclaration(
                name="symbol",
                type=LogicalType.STRING,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`.",
            ),
            FieldDeclaration(
                name="category",
                type=LogicalType.STRING,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`.",
            ),
            FieldDeclaration(
                name="point_size",
                type=LogicalType.FLOAT,
                nullable=False,
                has_default=True,
                default=0.0,
                immutable=False,
                description="Stores the size of one point for the asset.",
            ),
            FieldDeclaration(
                name="digits",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=True,
                default=0,
                immutable=False,
                description="Stores the number of decimal digits used for the asset's price.",
            ),
            FieldDeclaration(
                name="is_active",
                type=LogicalType.BOOLEAN,
                nullable=False,
                has_default=True,
                default=True,
                immutable=False,
                description="Indicates whether the asset is active.",
            ),
            FieldDeclaration(
                name="description",
                type=LogicalType.STRING,
                nullable=True,
                has_default=False,
                default=None,
                immutable=False,
                description="Describes the asset.",
            ),
        ),
        primary_key="id",
        relations=(Relation(local_field="broker_id", target_entity="Broker", target_field="id"),),
        unique_constraints=(("broker_id", "symbol"),),
        indexes=(),
    )

    id: int | None = Field(default=None, primary_key=True)
    broker_id: int
    symbol: str
    category: str
    point_size: Float = 0.0
    digits: int = 0
    is_active: bool = True
    description: str | None = None
