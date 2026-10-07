"""Asset Entity."""

from typing import ClassVar

from ..core._storage import realize_field, table_arguments, table_name
from ..core._types import FloatValue
from ..core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniquenessConstraint,
    ValueGeneration,
)
from ..core.foundation import Foundation

DECLARATION = Declaration(
    name="Asset",
    description="Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.",
    fields=(
        FieldDeclaration(
            name="id",
            type=FieldType.integer,
            nullable=False,
            description=None,
            immutable=True,
            value_generation=ValueGeneration.auto_increment,
        ),
        FieldDeclaration(
            name="broker_id",
            type=FieldType.integer,
            nullable=False,
            description="Identifies the broker that provides this asset.",
        ),
        FieldDeclaration(
            name="symbol",
            type=FieldType.string,
            nullable=False,
            description="Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`.",
        ),
        FieldDeclaration(
            name="category",
            type=FieldType.string,
            nullable=False,
            description="Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`.",
        ),
        FieldDeclaration(
            name="point_size",
            type=FieldType.float,
            nullable=False,
            description="Stores the size of one point for the asset.",
            default=0.0,
        ),
        FieldDeclaration(
            name="digits",
            type=FieldType.integer,
            nullable=False,
            description="Stores the number of decimal digits used for the asset's price.",
            default=0,
        ),
        FieldDeclaration(
            name="is_active",
            type=FieldType.boolean,
            nullable=False,
            description="Indicates whether the asset is active.",
            default=True,
        ),
        FieldDeclaration(
            name="description",
            type=FieldType.string,
            nullable=True,
            description="Describes the asset.",
        ),
    ),
    primary_key="id",
    relations=(
        Relation(local_field="broker_id", target_entity="Broker", target_field="id"),
    ),
    unique_constraints=(UniquenessConstraint(fields=("broker_id", "symbol")),),
)


class Asset(Foundation, table=True):
    __tablename__ = table_name(DECLARATION)
    __table_args__ = table_arguments(DECLARATION)

    declaration: ClassVar[Declaration] = DECLARATION

    id: int | None = realize_field(DECLARATION, "id")
    broker_id: int = realize_field(DECLARATION, "broker_id")
    symbol: str = realize_field(DECLARATION, "symbol")
    category: str = realize_field(DECLARATION, "category")
    point_size: FloatValue = realize_field(DECLARATION, "point_size")
    digits: int = realize_field(DECLARATION, "digits")
    is_active: bool = realize_field(DECLARATION, "is_active")
    description: str | None = realize_field(DECLARATION, "description")
