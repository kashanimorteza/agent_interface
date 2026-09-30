"""The Asset Entity."""

from typing import ClassVar

from model.core._entity import Entity
from model.core._fields import activity, identity
from model.core._types import Float
from model.core.declaration import Declaration as EntityDeclaration
from model.core.declaration import FieldDeclaration, Relation


class Asset(Entity):
    Declaration: ClassVar[EntityDeclaration] = EntityDeclaration(
        name="Asset",
        description=(
            "Defines an asset that can be selected for trading. "
            "It provides the system with the complete set of "
            "available tradable assets and identifies the "
            "category of each asset so the system knows exactly "
            "what is being traded."
        ),
        fields=(
            identity(),
            FieldDeclaration(
                "broker_id",
                "integer",
                nullable=False,
                description="Identifies the broker that provides this asset.",
            ),
            FieldDeclaration(
                "symbol",
                "string",
                nullable=False,
                description=(
                    "Identifies the tradable asset, such as `EUR/USD`, "
                    "`XAU/USD`, or `USOil`."
                ),
            ),
            FieldDeclaration(
                "category",
                "string",
                nullable=False,
                description=(
                    "Identifies the asset category, such as `Currency`, "
                    "`Commodity`, or `Cryptocurrency`."
                ),
            ),
            FieldDeclaration(
                "point_size",
                "float",
                nullable=False,
                description="Stores the size of one point for the asset.",
                has_default=True,
                default=0.0,
            ),
            FieldDeclaration(
                "digits",
                "integer",
                nullable=False,
                description=(
                    "Stores the number of decimal digits used for the asset's price."
                ),
                has_default=True,
                default=0,
            ),
            activity("Indicates whether the asset is active."),
            FieldDeclaration(
                "description",
                "string",
                nullable=True,
                description="Describes the asset.",
            ),
        ),
        primary_key="id",
        relations=(Relation("broker_id", "Broker", "id"),),
        unique_constraints=(("broker_id", "symbol"),),
    )

    id: int | None = None
    broker_id: int
    symbol: str
    category: str
    point_size: Float = 0.0
    digits: int = 0
    is_active: bool = True
    description: str | None = None
