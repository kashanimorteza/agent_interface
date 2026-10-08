"""The Asset Entity."""

from typing import ClassVar

from model.core._storage import realize_field, table_args
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    ValueGeneration,
)
from model.core.foundation import Foundation


class Asset(Foundation, table=True):
    __tablename__ = "Asset"
    declaration: ClassVar[Declaration] = Declaration(
        name="Asset",
        description="Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.",
        fields=(
            FieldDeclaration(
                "id",
                FieldType.integer,
                False,
                immutable=True,
                value_generation=ValueGeneration.auto_increment,
            ),
            FieldDeclaration(
                "broker_id",
                FieldType.integer,
                False,
                description="Identifies the broker that provides this asset.",
            ),
            FieldDeclaration(
                "symbol",
                FieldType.string,
                False,
                description="Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`.",
            ),
            FieldDeclaration(
                "category",
                FieldType.string,
                False,
                description="Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`.",
            ),
            FieldDeclaration(
                "point_size",
                FieldType.float,
                False,
                description="Stores the size of one point for the asset.",
                default=0.0,
            ),
            FieldDeclaration(
                "digits",
                FieldType.integer,
                False,
                description="Stores the number of decimal digits used for the asset's price.",
                default=0,
            ),
            FieldDeclaration(
                "is_active",
                FieldType.boolean,
                False,
                description="Indicates whether the asset is active.",
                default=True,
            ),
            FieldDeclaration(
                "description",
                FieldType.string,
                True,
                description="Describes the asset.",
            ),
        ),
        primary_key="id",
        relations=(Relation("broker_id", "Broker", "id"),),
        unique_constraints=(("broker_id", "symbol"),),
    )
    __table_args__ = table_args(declaration)

    id: int | None = realize_field(declaration, "id")
    broker_id: int = realize_field(declaration, "broker_id")
    symbol: str = realize_field(declaration, "symbol")
    category: str = realize_field(declaration, "category")
    point_size: float = realize_field(declaration, "point_size")
    digits: int = realize_field(declaration, "digits")
    is_active: bool = realize_field(declaration, "is_active")
    description: str | None = realize_field(declaration, "description")
