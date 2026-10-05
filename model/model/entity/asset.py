from typing import ClassVar

from sqlalchemy import Identity, UniqueConstraint
from sqlmodel import Field

from model.core._base import EntityBase
from model.core.declaration import Declaration, FieldDeclaration, Relation


class Asset(EntityBase, table=True):
    __table_args__ = (
        UniqueConstraint("broker_id", "symbol"),
        {"sqlite_autoincrement": True},
    )
    declaration: ClassVar[Declaration] = Declaration(
        "Asset",
        "Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.",
        (
            FieldDeclaration("id", None, "integer", False, immutable=True, value_generation="auto_increment"),
            FieldDeclaration("broker_id", "Identifies the broker that provides this asset.", "integer", False),
            FieldDeclaration(
                "symbol", "Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`.", "string", False
            ),
            FieldDeclaration(
                "category",
                "Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`.",
                "string",
                False,
            ),
            FieldDeclaration(
                "point_size",
                "Stores the size of one point for the asset.",
                "float",
                False,
                has_default=True,
                default=0.0,
            ),
            FieldDeclaration(
                "digits",
                "Stores the number of decimal digits used for the asset's price.",
                "integer",
                False,
                has_default=True,
                default=0,
            ),
            FieldDeclaration(
                "is_active", "Indicates whether the asset is active.", "boolean", False, has_default=True, default=True
            ),
            FieldDeclaration("description", "Describes the asset.", "string", True),
        ),
        "id",
        relations=(Relation("broker_id", "Broker", "id"),),
        unique_constraints=(
            (
                "broker_id",
                "symbol",
            ),
        ),
    )
    id: int | None = Field(default=None, primary_key=True, sa_column_args=[Identity()])
    broker_id: int = Field(foreign_key="Broker.id", description="Identifies the broker that provides this asset.")
    symbol: str = Field(description="Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`.")
    category: str = Field(
        description="Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`."
    )
    point_size: float = Field(default=0.0, description="Stores the size of one point for the asset.")
    digits: int = Field(default=0, description="Stores the number of decimal digits used for the asset's price.")
    is_active: bool = Field(default=True, description="Indicates whether the asset is active.")
    description: str | None = Field(default=None, description="Describes the asset.")
