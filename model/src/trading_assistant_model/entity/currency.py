from typing import ClassVar

from sqlmodel import Field

from ..declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Reference,
    UniqueConstraint,
    ValueGeneration,
)
from ..foundation import Foundation


class Currency(Foundation, table=True):
    """Defines a currency that can be used by the trading system and identifies its
    standard code, display symbol, associated country or region, and monetary decimal
    precision.
    """

    declaration: ClassVar[Declaration] = Declaration(
        entity="Currency",
        fields=(
            FieldDeclaration(
                "id",
                FieldType.INTEGER,
                nullable=False,
                generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration("user_id", FieldType.INTEGER, nullable=False),
            FieldDeclaration("code", FieldType.STRING, nullable=False, length=3),
            FieldDeclaration("symbol", FieldType.STRING, nullable=True),
            FieldDeclaration("country", FieldType.STRING, nullable=True),
            FieldDeclaration(
                "decimal_digits", FieldType.INTEGER, nullable=False, default=2
            ),
            FieldDeclaration(
                "is_active", FieldType.BOOLEAN, nullable=False, default=True
            ),
            FieldDeclaration("description", FieldType.STRING, nullable=True),
        ),
        primary_key=("id",),
        unique_constraints=(UniqueConstraint(("user_id", "code")),),
        references=(Reference(("user_id",), "User", ("id",)),),
    )

    id: int | None = Field(
        default=None,
        primary_key=True,
        description="Unique identifier of the currency, assigned automatically.",
    )
    user_id: int = Field(description="Identifies the user who owns this currency.")
    code: str = Field(
        max_length=3,
        description="The currency's standard three-letter code, such as `USD` or `EUR`.",
    )
    symbol: str | None = Field(
        default=None,
        description="The currency's display symbol, such as `$`, `€`, or `£`.",
    )
    country: str | None = Field(
        default=None,
        description="Identifies the country or region associated with the currency.",
    )
    decimal_digits: int = Field(
        default=2,
        description="Defines the number of decimal digits normally used for monetary values in the currency.",
    )
    is_active: bool = Field(
        default=True, description="Indicates whether the currency is active."
    )
    description: str | None = Field(default=None, description="Describes the currency.")
