"""The Currency Entity."""

from typing import ClassVar

from model.core._storage import realize_field, table_args
from model.core.declaration import (
    Declaration,
    FieldConstraints,
    FieldDeclaration,
    FieldType,
    Relation,
    ValueGeneration,
)
from model.core.foundation import Foundation


class Currency(Foundation, table=True):
    __tablename__ = "Currency"
    declaration: ClassVar[Declaration] = Declaration(
        name="Currency",
        description="Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.",
        fields=(
            FieldDeclaration(
                "id",
                FieldType.integer,
                False,
                immutable=True,
                value_generation=ValueGeneration.auto_increment,
            ),
            FieldDeclaration(
                "user_id",
                FieldType.integer,
                False,
                description="Identifies the user who owns this currency.",
            ),
            FieldDeclaration(
                "code",
                FieldType.string,
                False,
                description="The currency's standard three-letter code, such as `USD` or `EUR`.",
                constraints=FieldConstraints(size=3),
            ),
            FieldDeclaration(
                "symbol",
                FieldType.string,
                True,
                description="The currency's display symbol, such as `$`, `€`, or `£`.",
            ),
            FieldDeclaration(
                "country",
                FieldType.string,
                True,
                description="Identifies the country or region associated with the currency.",
            ),
            FieldDeclaration(
                "decimal_digits",
                FieldType.integer,
                False,
                description="Defines the number of decimal digits normally used for monetary values in the currency.",
                default=2,
            ),
            FieldDeclaration(
                "is_active",
                FieldType.boolean,
                False,
                description="Indicates whether the currency is active.",
                default=True,
            ),
            FieldDeclaration(
                "description",
                FieldType.string,
                True,
                description="Describes the currency.",
            ),
        ),
        primary_key="id",
        relations=(Relation("user_id", "User", "id"),),
        unique_constraints=(("user_id", "code"),),
    )
    __table_args__ = table_args(declaration)

    id: int | None = realize_field(declaration, "id")
    user_id: int = realize_field(declaration, "user_id")
    code: str = realize_field(declaration, "code")
    symbol: str | None = realize_field(declaration, "symbol")
    country: str | None = realize_field(declaration, "country")
    decimal_digits: int = realize_field(declaration, "decimal_digits")
    is_active: bool = realize_field(declaration, "is_active")
    description: str | None = realize_field(declaration, "description")
