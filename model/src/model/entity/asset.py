"""The Asset Entity."""

from typing import ClassVar

from sqlmodel import Field
from sqlmodel import UniqueConstraint as TableUniqueConstraint

from model.core.base import Entity
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniqueConstraint,
    ValueGeneration,
)


class Asset(Entity, table=True):
    """The Asset Entity."""

    declaration: ClassVar[Declaration] = Declaration(
        name="Asset",
        description="Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.",
        fields=(
            FieldDeclaration(
                name="id",
                type=FieldType.INTEGER,
                nullable=False,
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
                description="Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`.",
            ),
            FieldDeclaration(
                name="category",
                type=FieldType.STRING,
                nullable=False,
                description="Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`.",
            ),
            FieldDeclaration(
                name="point_size",
                type=FieldType.FLOAT,
                nullable=False,
                description="Stores the size of one point for the asset.",
                has_default=True,
                default=0.0,
            ),
            FieldDeclaration(
                name="digits",
                type=FieldType.INTEGER,
                nullable=False,
                description="Stores the number of decimal digits used for the asset's price.",
                has_default=True,
                default=0,
            ),
            FieldDeclaration(
                name="is_active",
                type=FieldType.BOOLEAN,
                nullable=False,
                description="Indicates whether the asset is active.",
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type=FieldType.STRING,
                nullable=True,
                description="Describes the asset.",
            ),
        ),
        primary_key="id",
        relations=(
            Relation(
                local_field="broker_id", target_entity="Broker", target_field="id"
            ),
        ),
        unique_constraints=(UniqueConstraint(fields=("broker_id", "symbol")),),
    )

    __table_args__ = (TableUniqueConstraint("broker_id", "symbol"),)

    id: int | None = Field(default=None, primary_key=True)
    broker_id: int
    symbol: str
    category: str
    point_size: float = 0.0
    digits: int = 0
    is_active: bool = True
    description: str | None = None
