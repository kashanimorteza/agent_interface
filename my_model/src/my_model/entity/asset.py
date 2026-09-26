"""Asset Domain Entity."""

from typing import ClassVar

from sqlmodel import Field, UniqueConstraint

from my_model.model_declaration import (
    FieldDeclaration,
    LogicalType,
    ModelDeclaration,
    ReferenceDeclaration,
    ValueGeneration,
)
from my_model.model_foundation import ModelFoundation


class Asset(ModelFoundation, table=True):
    """Defines an asset that can be selected for trading."""

    declaration: ClassVar[ModelDeclaration] = ModelDeclaration(
        entity="Asset",
        fields=(
            FieldDeclaration(
                "id", LogicalType.INTEGER, generation=ValueGeneration.AUTO_INCREMENT
            ),
            FieldDeclaration("broker_id", LogicalType.INTEGER),
            FieldDeclaration("symbol", LogicalType.STRING),
            FieldDeclaration("category", LogicalType.STRING),
            FieldDeclaration("point_size", LogicalType.FLOAT, default=0.0),
            FieldDeclaration("digits", LogicalType.INTEGER, default=0),
            FieldDeclaration("is_active", LogicalType.BOOLEAN, default=True),
            FieldDeclaration("description", LogicalType.STRING, nullable=True),
        ),
        primary_key=("id",),
        references=(ReferenceDeclaration("broker_id", "Broker"),),
        unique_constraints=(("broker_id", "symbol"),),
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
