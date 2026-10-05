from typing import ClassVar

from model.core.base import Entity
from model.core.columns import column, table_arguments
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    RelationDeclaration,
    UniqueConstraintDeclaration,
    activity,
    identity,
)

_DECLARATION = Declaration(
    name="Asset",
    description="Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.",
    fields=(
        identity(),
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
            default=0.0,
        ),
        FieldDeclaration(
            name="digits",
            description="Stores the number of decimal digits used for the asset's price.",
            type=FieldType.INTEGER,
            nullable=False,
            default=0,
        ),
        activity("Indicates whether the asset is active."),
        FieldDeclaration(
            name="description",
            description="Describes the asset.",
            type=FieldType.STRING,
            nullable=True,
        ),
    ),
    primary_key="id",
    relations=(RelationDeclaration("broker_id", "Broker", "id"),),
    unique_constraints=(
        UniqueConstraintDeclaration(
            (
                "broker_id",
                "symbol",
            )
        ),
    ),
)


class Asset(Entity, table=True):
    __table_args__ = table_arguments(_DECLARATION)
    declaration: ClassVar[Declaration] = _DECLARATION

    id: int | None = column(_DECLARATION, "id")
    broker_id: int = column(_DECLARATION, "broker_id")
    symbol: str = column(_DECLARATION, "symbol")
    category: str = column(_DECLARATION, "category")
    point_size: float = column(_DECLARATION, "point_size")
    digits: int = column(_DECLARATION, "digits")
    is_active: bool = column(_DECLARATION, "is_active")
    description: str | None = column(_DECLARATION, "description")
