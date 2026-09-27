"""The Asset Entity."""

from typing import ClassVar

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from my_model.model_declaration import (
    FieldDeclaration,
    Model_Declaration,
    ReferenceDeclaration,
)
from my_model.model_foundation import Model_Foundation


class Asset(Model_Foundation, table=True):
    """An asset that can be selected for trading, with its category."""

    declaration: ClassVar[Model_Declaration] = Model_Declaration(
        entity="Asset",
        purpose="An asset that can be selected for trading, with its category.",
        fields=(
            FieldDeclaration(
                name="id",
                type="integer",
                nullable=False,
                value_generation="auto_increment",
            ),
            FieldDeclaration(
                name="broker_id",
                type="integer",
                nullable=False,
                purpose="Identifies the broker that provides this asset.",
            ),
            FieldDeclaration(
                name="symbol",
                type="string",
                nullable=False,
                purpose="Identifies the tradable asset.",
            ),
            FieldDeclaration(
                name="category",
                type="string",
                nullable=False,
                purpose="Identifies the asset category, such as Currency, Commodity, or Cryptocurrency.",
            ),
            FieldDeclaration(
                name="point_size",
                type="float",
                nullable=False,
                purpose="The size of one point for the asset.",
                has_default=True,
                default=0.0,
            ),
            FieldDeclaration(
                name="digits",
                type="integer",
                nullable=False,
                purpose="The number of decimal digits used for the asset's price.",
                has_default=True,
                default=0,
            ),
            FieldDeclaration(
                name="is_active",
                type="boolean",
                nullable=False,
                purpose="Indicates whether the asset is active.",
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type="string",
                nullable=True,
                purpose="Describes the asset.",
            ),
        ),
        references=(ReferenceDeclaration(field="broker_id", entity="Broker"),),
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
