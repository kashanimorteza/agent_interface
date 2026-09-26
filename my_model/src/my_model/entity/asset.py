"""Asset Entity."""

from typing import ClassVar

from sqlmodel import Field, UniqueConstraint

from my_model.model_declaration import (
    FieldDeclaration,
    LogicalType,
    ModelDeclaration,
    Reference,
    RelationshipKind,
    UniquenessConstraint,
    ValueGeneration,
)
from my_model.model_foundation import ModelFoundation


class Asset(ModelFoundation, table=True):
    """Defines an asset that can be selected for trading."""

    declaration: ClassVar[ModelDeclaration] = ModelDeclaration(
        entity="Asset",
        purpose="Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.",
        fields=(
            FieldDeclaration(
                "id",
                LogicalType.INTEGER,
                generation=ValueGeneration.AUTO_INCREMENT,
                purpose="",
            ),
            FieldDeclaration(
                "broker_id",
                LogicalType.INTEGER,
                purpose="Identifies the broker that provides this asset",
            ),
            FieldDeclaration(
                "symbol",
                LogicalType.STRING,
                purpose="Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`",
            ),
            FieldDeclaration(
                "category",
                LogicalType.STRING,
                purpose="Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`",
            ),
            FieldDeclaration(
                "point_size",
                LogicalType.FLOAT,
                has_default=True,
                default=0.0,
                purpose="Stores the size of one point for the asset",
            ),
            FieldDeclaration(
                "digits",
                LogicalType.INTEGER,
                has_default=True,
                default=0,
                purpose="Stores the number of decimal digits used for the asset's price",
            ),
            FieldDeclaration(
                "is_active",
                LogicalType.BOOLEAN,
                has_default=True,
                default=True,
                purpose="Indicates whether the asset is active",
            ),
            FieldDeclaration(
                "description",
                LogicalType.STRING,
                nullable=True,
                purpose="Describes the asset",
            ),
        ),
        references=(
            Reference("broker_id", "Broker", "id", RelationshipKind.BELONGS_TO),
        ),
        unique_constraints=(
            UniquenessConstraint(
                (
                    "broker_id",
                    "symbol",
                )
            ),
        ),
    )
    __table_args__ = (UniqueConstraint("broker_id", "symbol"),)

    id: int | None = Field(default=None, primary_key=True)
    broker_id: int = Field(foreign_key="broker.id")
    symbol: str
    category: str
    point_size: float = 0.0
    digits: int = 0
    is_active: bool = True
    description: str | None = None
