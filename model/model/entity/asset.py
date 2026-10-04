"""The Asset Entity."""

from sqlmodel import Field

from model.core._base import Entity
from model.core._defaults import (
    activity_declaration,
    activity_field,
    identity_declaration,
    identity_field,
)
from model.core._storage import table_arguments
from model.core.declaration import Declaration, FieldDeclaration, RelationDeclaration


class Asset(Entity, table=True):
    """The Asset Entity."""

    __tablename__ = "Asset"  # pyright: ignore[reportAssignmentType]
    __table_args__ = table_arguments(
        ("broker_id", "symbol"),
    )

    declaration = Declaration(
        name="Asset",
        description="Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.",
        fields=(
            identity_declaration(),
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
                default=0.0,
            ),
            FieldDeclaration(
                name="digits",
                description="Stores the number of decimal digits used for the asset's price.",
                type="integer",
                nullable=False,
                default=0,
            ),
            activity_declaration("Indicates whether the asset is active."),
            FieldDeclaration(
                name="description",
                description="Describes the asset.",
                type="string",
                nullable=True,
            ),
        ),
        primary_key="id",
        relations=(
            RelationDeclaration(
                local_field="broker_id", target_entity="Broker", target_field="id"
            ),
        ),
        unique_constraints=(("broker_id", "symbol"),),
    )

    id: int | None = identity_field()
    broker_id: int = Field(
        foreign_key="Broker.id",
        description="Identifies the broker that provides this asset.",
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
    is_active: bool = activity_field("Indicates whether the asset is active.")
    description: str | None = Field(default=None, description="Describes the asset.")
