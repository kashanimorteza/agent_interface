"""Currency Entity."""

from typing import ClassVar

from ..core._storage import realize_field, table_arguments, table_name
from ..core.declaration import (
    Declaration,
    FieldConstraints,
    FieldDeclaration,
    FieldType,
    Relation,
    UniquenessConstraint,
    ValueGeneration,
)
from ..core.foundation import Foundation

DECLARATION = Declaration(
    name="Currency",
    description="Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.",
    fields=(
        FieldDeclaration(
            name="id",
            type=FieldType.integer,
            nullable=False,
            description=None,
            immutable=True,
            value_generation=ValueGeneration.auto_increment,
        ),
        FieldDeclaration(
            name="user_id",
            type=FieldType.integer,
            nullable=False,
            description="Identifies the user who owns this currency.",
        ),
        FieldDeclaration(
            name="code",
            type=FieldType.string,
            nullable=False,
            description="The currency's standard three-letter code, such as `USD` or `EUR`.",
            constraints=FieldConstraints(size=3),
        ),
        FieldDeclaration(
            name="symbol",
            type=FieldType.string,
            nullable=True,
            description="The currency's display symbol, such as `$`, `€`, or `£`.",
        ),
        FieldDeclaration(
            name="country",
            type=FieldType.string,
            nullable=True,
            description="Identifies the country or region associated with the currency.",
        ),
        FieldDeclaration(
            name="decimal_digits",
            type=FieldType.integer,
            nullable=False,
            description="Defines the number of decimal digits normally used for monetary values in the currency.",
            default=2,
        ),
        FieldDeclaration(
            name="is_active",
            type=FieldType.boolean,
            nullable=False,
            description="Indicates whether the currency is active.",
            default=True,
        ),
        FieldDeclaration(
            name="description",
            type=FieldType.string,
            nullable=True,
            description="Describes the currency.",
        ),
    ),
    primary_key="id",
    relations=(
        Relation(local_field="user_id", target_entity="User", target_field="id"),
    ),
    unique_constraints=(UniquenessConstraint(fields=("user_id", "code")),),
)


class Currency(Foundation, table=True):
    __tablename__ = table_name(DECLARATION)
    __table_args__ = table_arguments(DECLARATION)

    declaration: ClassVar[Declaration] = DECLARATION

    id: int | None = realize_field(DECLARATION, "id")
    user_id: int = realize_field(DECLARATION, "user_id")
    code: str = realize_field(DECLARATION, "code")
    symbol: str | None = realize_field(DECLARATION, "symbol")
    country: str | None = realize_field(DECLARATION, "country")
    decimal_digits: int = realize_field(DECLARATION, "decimal_digits")
    is_active: bool = realize_field(DECLARATION, "is_active")
    description: str | None = realize_field(DECLARATION, "description")
