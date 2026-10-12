"""The Asset Entity."""

from typing import ClassVar

from model.core._storage import mapped_field, table_arguments
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniquenessConstraint,
    ValueGeneration,
)
from model.core.foundation import Foundation


class Asset(Foundation, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="Asset",
        description=(
            "Defines an asset that can be selected for trading. It provides the system with the "
            "complete set of available tradable assets and identifies the category of each asset "
            "so the system knows exactly what is being traded."
        ),
        fields=(
            FieldDeclaration(
                name="id",
                type=FieldType.INTEGER,
                nullable=False,
                immutable=True,
                value_generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration(
                name="broker_id",
                type=FieldType.INTEGER,
                nullable=False,
                description="Identifies the broker that provides this asset.",
            ),
            FieldDeclaration(
                name="symbol",
                type=FieldType.STRING,
                nullable=False,
                description=(
                    "Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`."
                ),
            ),
            FieldDeclaration(
                name="category",
                type=FieldType.STRING,
                nullable=False,
                description=(
                    "Identifies the asset category, such as `Currency`, `Commodity`, or "
                    "`Cryptocurrency`."
                ),
            ),
            FieldDeclaration(
                name="point_size",
                type=FieldType.FLOAT,
                nullable=False,
                description="Stores the size of one point for the asset.",
                default=0.0,
            ),
            FieldDeclaration(
                name="digits",
                type=FieldType.INTEGER,
                nullable=False,
                description="Stores the number of decimal digits used for the asset's price.",
                default=0,
            ),
            FieldDeclaration(
                name="is_active",
                type=FieldType.BOOLEAN,
                nullable=False,
                description="Indicates whether the asset is active.",
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type=FieldType.STRING,
                nullable=True,
                description="Describes the asset.",
            ),
        ),
        relations=(Relation("broker_id", "Broker", "id"),),
        unique_constraints=(UniquenessConstraint(("broker_id", "symbol")),),
    )

    __tablename__ = "Asset"
    __table_args__ = table_arguments(declaration)

    id: int | None = mapped_field(declaration, "id")
    broker_id: int = mapped_field(declaration, "broker_id")
    symbol: str = mapped_field(declaration, "symbol")
    category: str = mapped_field(declaration, "category")
    point_size: float = mapped_field(declaration, "point_size")
    digits: int = mapped_field(declaration, "digits")
    is_active: bool = mapped_field(declaration, "is_active")
    description: str | None = mapped_field(declaration, "description")
