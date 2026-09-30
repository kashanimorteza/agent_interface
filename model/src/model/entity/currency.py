"""The Currency Entity."""

from types import MappingProxyType
from typing import ClassVar

from sqlmodel import Field

from ..core.base import EntityBase
from ..core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    ValueGeneration,
)


class Currency(EntityBase):
    """The Currency Entity; its Declaration states its complete meaning."""

    declaration: ClassVar[Declaration] = Declaration(
        name="Currency",
        description="Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.",
        fields=(
            FieldDeclaration(
                name="id",
                description=None,
                type=FieldType.INTEGER,
                nullable=False,
                immutable=True,
                value_generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration(
                name="user_id",
                description="Identifies the user who owns this currency.",
                type=FieldType.INTEGER,
                nullable=False,
            ),
            FieldDeclaration(
                name="code",
                description="The currency's standard three-letter code, such as `USD` or `EUR`.",
                type=FieldType.STRING,
                nullable=False,
                constraints=MappingProxyType({"size": 3}),
            ),
            FieldDeclaration(
                name="symbol",
                description="The currency's display symbol, such as `$`, `€`, or `£`.",
                type=FieldType.STRING,
                nullable=True,
            ),
            FieldDeclaration(
                name="country",
                description="Identifies the country or region associated with the currency.",
                type=FieldType.STRING,
                nullable=True,
            ),
            FieldDeclaration(
                name="decimal_digits",
                description="Defines the number of decimal digits normally used for monetary values in the currency.",
                type=FieldType.INTEGER,
                nullable=False,
                has_default=True,
                default=2,
            ),
            FieldDeclaration(
                name="is_active",
                description="Indicates whether the currency is active.",
                type=FieldType.BOOLEAN,
                nullable=False,
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                description="Describes the currency.",
                type=FieldType.STRING,
                nullable=True,
            ),
        ),
        primary_key="id",
        relations=(Relation("user_id", "User", "id"),),
        unique_constraints=(("user_id", "code"),),
    )

    id: int | None = None
    user_id: int
    code: str = Field(min_length=3, max_length=3)
    symbol: str | None = None
    country: str | None = None
    decimal_digits: int = 2
    is_active: bool = True
    description: str | None = None
