"""The Asset Entity."""

from typing import ClassVar

from sqlmodel import Field

from model.core.base import Entity
from model.core.declaration import Declaration, FieldDeclaration, Relation
from model.core.storage import column_options, table_args

_DECLARATION = Declaration(
    name="Asset",
    description="Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.",
    fields=(
        FieldDeclaration(
            name="id",
            description=None,
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
    relations=(
        Relation(local_field="broker_id", target_entity="Broker", target_field="id"),
    ),
    unique_constraints=(("broker_id", "symbol"),),
    indexes=(),
)


class Asset(Entity, table=True):
    __table_args__ = table_args(_DECLARATION)
    declaration: ClassVar[Declaration] = _DECLARATION

    id: int | None = Field(default=None, **column_options(_DECLARATION, "id"))
    broker_id: int = Field(
        description="Identifies the broker that provides this asset.",
        **column_options(_DECLARATION, "broker_id"),
    )
    symbol: str = Field(
        description="Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`.",
        **column_options(_DECLARATION, "symbol"),
    )
    category: str = Field(
        description="Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`.",
        **column_options(_DECLARATION, "category"),
    )
    point_size: float = Field(
        default=0.0,
        description="Stores the size of one point for the asset.",
        **column_options(_DECLARATION, "point_size"),
    )
    digits: int = Field(
        default=0,
        description="Stores the number of decimal digits used for the asset's price.",
        **column_options(_DECLARATION, "digits"),
    )
    is_active: bool = Field(
        default=True,
        description="Indicates whether the asset is active.",
        **column_options(_DECLARATION, "is_active"),
    )
    description: str | None = Field(
        default=None,
        description="Describes the asset.",
        **column_options(_DECLARATION, "description"),
    )
