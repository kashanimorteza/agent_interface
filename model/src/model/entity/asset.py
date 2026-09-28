"""Asset Entity."""

from typing import ClassVar

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from model.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Generation,
    Reference,
    Unique,
)
from model.foundation import Foundation


class Asset(Foundation, table=True):
    """Tradable asset provided by a broker, with its category."""

    declaration: ClassVar[Declaration] = Declaration(
        entity="Asset",
        fields=(
            FieldDeclaration(
                "id", FieldType.INTEGER, generation=Generation.AUTO_INCREMENT
            ),
            FieldDeclaration("broker_id", FieldType.INTEGER),
            FieldDeclaration("symbol", FieldType.STRING),
            FieldDeclaration("category", FieldType.STRING),
            FieldDeclaration("point_size", FieldType.FLOAT, default=0.0),
            FieldDeclaration("digits", FieldType.INTEGER, default=0),
            FieldDeclaration("is_active", FieldType.BOOLEAN, default=True),
            FieldDeclaration("description", FieldType.STRING, nullable=True),
        ),
        references=(Reference("broker_id", "Broker"),),
        uniques=(Unique(("broker_id", "symbol")),),
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
