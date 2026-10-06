"""The Asset Entity."""

from typing import ClassVar

from model.core._storage import column, table_args
from model.core._types import FiniteFloat
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniqueConstraint,
    ValueGeneration,
)
from model.core.foundation import Foundation

_DECLARATION = Declaration(
    name="Asset",
    description=(
        "Defines an asset that can be selected for trading. It provides the "
        "system with the complete set of available tradable assets and "
        "identifies the category of each asset so the system knows exactly "
        "what is being traded."
    ),
    fields=(
        FieldDeclaration(
            name="id",
            type=FieldType.integer,
            nullable=False,
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
            description=(
                "Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`."
            ),
        ),
        FieldDeclaration(
            name="category",
            type=FieldType.string,
            nullable=False,
            description=(
                "Identifies the asset category, such as `Currency`, `Commodity`, or "
                "`Cryptocurrency`."
            ),
        ),
        FieldDeclaration(
            name="point_size",
            type=FieldType.float,
            nullable=False,
            description="Stores the size of one point for the asset.",
            has_default=True,
            default=0.0,
        ),
        FieldDeclaration(
            name="digits",
            type=FieldType.integer,
            nullable=False,
            description="Stores the number of decimal digits used for the asset's price.",
            has_default=True,
            default=0,
        ),
        FieldDeclaration(
            name="is_active",
            type=FieldType.boolean,
            nullable=False,
            description="Indicates whether the asset is active.",
            has_default=True,
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
    relations=(Relation(local_field="broker_id", target_entity="Broker", target_field="id"),),
    unique_constraints=(UniqueConstraint(fields=("broker_id", "symbol")),),
)


class Asset(Foundation, table=True):
    """Asset."""

    __tablename__ = "Asset"  # pyright: ignore[reportAssignmentType]
    declaration: ClassVar[Declaration] = _DECLARATION
    __table_args__ = table_args(_DECLARATION)

    id: int | None = column(_DECLARATION, "id")
    broker_id: int = column(_DECLARATION, "broker_id")
    symbol: str = column(_DECLARATION, "symbol")
    category: str = column(_DECLARATION, "category")
    point_size: FiniteFloat = column(_DECLARATION, "point_size")
    digits: int = column(_DECLARATION, "digits")
    is_active: bool = column(_DECLARATION, "is_active")
    description: str | None = column(_DECLARATION, "description")
