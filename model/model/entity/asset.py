"""The Asset Entity."""

from typing import ClassVar

from model.core._storage import realize_field, table_args
from model.core.declaration import (
    EntityDeclaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniqueConstraint,
    ValueGeneration,
)
from model.core.foundation import Foundation

DECLARATION = EntityDeclaration(
    name="Asset",
    description="Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.",
    fields=(
        FieldDeclaration(
            "id",
            FieldType.integer,
            nullable=False,
            immutable=True,
            value_generation=ValueGeneration.auto_increment,
        ),
        FieldDeclaration(
            "broker_id",
            FieldType.integer,
            nullable=False,
            description="Identifies the broker that provides this asset.",
        ),
        FieldDeclaration(
            "symbol",
            FieldType.string,
            nullable=False,
            description="Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`.",
        ),
        FieldDeclaration(
            "category",
            FieldType.string,
            nullable=False,
            description="Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`.",
        ),
        FieldDeclaration(
            "point_size",
            FieldType.float,
            nullable=False,
            description="Stores the size of one point for the asset.",
            default=0.0,
        ),
        FieldDeclaration(
            "digits",
            FieldType.integer,
            nullable=False,
            description="Stores the number of decimal digits used for the asset's price.",
            default=0,
        ),
        FieldDeclaration(
            "is_active",
            FieldType.boolean,
            nullable=False,
            description="Indicates whether the asset is active.",
            default=True,
        ),
        FieldDeclaration(
            "description",
            FieldType.string,
            nullable=True,
            description="Describes the asset.",
        ),
    ),
    relations=(Relation("broker_id", "Broker", "id"),),
    unique_constraints=(UniqueConstraint(("broker_id", "symbol")),),
)


class Asset(Foundation, table=True):
    __tablename__ = "Asset"
    __table_args__ = table_args(DECLARATION)

    declaration: ClassVar[EntityDeclaration] = DECLARATION

    id: int | None = realize_field(DECLARATION, "id")
    broker_id: int = realize_field(DECLARATION, "broker_id")
    symbol: str = realize_field(DECLARATION, "symbol")
    category: str = realize_field(DECLARATION, "category")
    point_size: float = realize_field(DECLARATION, "point_size")
    digits: int = realize_field(DECLARATION, "digits")
    is_active: bool = realize_field(DECLARATION, "is_active")
    description: str | None = realize_field(DECLARATION, "description")
