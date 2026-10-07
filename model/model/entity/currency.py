"""The Currency Entity."""

from typing import ClassVar

from model.core._storage import realize_field, table_args
from model.core.declaration import (
    EntityDeclaration,
    FieldConstraints,
    FieldDeclaration,
    FieldType,
    Relation,
    UniqueConstraint,
    ValueGeneration,
)
from model.core.foundation import Foundation

DECLARATION = EntityDeclaration(
    name="Currency",
    description="Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.",
    fields=(
        FieldDeclaration(
            "id",
            FieldType.integer,
            nullable=False,
            immutable=True,
            value_generation=ValueGeneration.auto_increment,
        ),
        FieldDeclaration(
            "user_id",
            FieldType.integer,
            nullable=False,
            description="Identifies the user who owns this currency.",
        ),
        FieldDeclaration(
            "code",
            FieldType.string,
            nullable=False,
            description="The currency's standard three-letter code, such as `USD` or `EUR`.",
            constraints=FieldConstraints(size=3),
        ),
        FieldDeclaration(
            "symbol",
            FieldType.string,
            nullable=True,
            description="The currency's display symbol, such as `$`, `€`, or `£`.",
        ),
        FieldDeclaration(
            "country",
            FieldType.string,
            nullable=True,
            description="Identifies the country or region associated with the currency.",
        ),
        FieldDeclaration(
            "decimal_digits",
            FieldType.integer,
            nullable=False,
            description="Defines the number of decimal digits normally used for monetary values in the currency.",
            default=2,
        ),
        FieldDeclaration(
            "is_active",
            FieldType.boolean,
            nullable=False,
            description="Indicates whether the currency is active.",
            default=True,
        ),
        FieldDeclaration(
            "description",
            FieldType.string,
            nullable=True,
            description="Describes the currency.",
        ),
    ),
    relations=(Relation("user_id", "User", "id"),),
    unique_constraints=(UniqueConstraint(("user_id", "code")),),
)


class Currency(Foundation, table=True):
    __tablename__ = "Currency"
    __table_args__ = table_args(DECLARATION)

    declaration: ClassVar[EntityDeclaration] = DECLARATION

    id: int | None = realize_field(DECLARATION, "id")
    user_id: int = realize_field(DECLARATION, "user_id")
    code: str = realize_field(DECLARATION, "code")
    symbol: str | None = realize_field(DECLARATION, "symbol")
    country: str | None = realize_field(DECLARATION, "country")
    decimal_digits: int = realize_field(DECLARATION, "decimal_digits")
    is_active: bool = realize_field(DECLARATION, "is_active")
    description: str | None = realize_field(DECLARATION, "description")
