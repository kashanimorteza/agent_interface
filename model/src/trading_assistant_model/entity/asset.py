from typing import ClassVar

from sqlmodel import Field

from ..declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Reference,
    UniqueConstraint,
    ValueGeneration,
)
from ..foundation import Foundation


class Asset(Foundation, table=True):
    """Defines an asset that can be selected for trading. It provides the system with the
    complete set of available tradable assets and identifies the category of each asset
    so the system knows exactly what is being traded.
    """

    declaration: ClassVar[Declaration] = Declaration(
        entity="Asset",
        fields=(
            FieldDeclaration(
                "id",
                FieldType.INTEGER,
                nullable=False,
                generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration("broker_id", FieldType.INTEGER, nullable=False),
            FieldDeclaration("symbol", FieldType.STRING, nullable=False),
            FieldDeclaration("category", FieldType.STRING, nullable=False),
            FieldDeclaration(
                "point_size", FieldType.FLOAT, nullable=False, default=0.0
            ),
            FieldDeclaration("digits", FieldType.INTEGER, nullable=False, default=0),
            FieldDeclaration(
                "is_active", FieldType.BOOLEAN, nullable=False, default=True
            ),
            FieldDeclaration("description", FieldType.STRING, nullable=True),
        ),
        primary_key=("id",),
        unique_constraints=(UniqueConstraint(("broker_id", "symbol")),),
        references=(Reference(("broker_id",), "Broker", ("id",)),),
    )

    id: int | None = Field(
        default=None,
        primary_key=True,
        description="Unique identifier of the asset, assigned automatically.",
    )
    broker_id: int = Field(
        description="Identifies the broker that provides this asset."
    )
    symbol: str = Field(
        description="Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`."
    )
    category: str = Field(
        description="Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`."
    )
    point_size: float = Field(
        default=0.0, description="Stores the size of one point for the asset."
    )
    digits: int = Field(
        default=0,
        description="Stores the number of decimal digits used for the asset's price.",
    )
    is_active: bool = Field(
        default=True, description="Indicates whether the asset is active."
    )
    description: str | None = Field(default=None, description="Describes the asset.")
