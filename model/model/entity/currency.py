"""The Currency Entity."""

from typing import ClassVar

from model.core._storage import column, table_args
from model.core.declaration import (
    Declaration,
    FieldConstraints,
    FieldDeclaration,
    FieldType,
    Relation,
    UniqueConstraint,
    ValueGeneration,
)
from model.core.foundation import Foundation

_DECLARATION = Declaration(
    name="Currency",
    description=(
        "Defines a currency that can be used by the trading system and "
        "identifies its standard code, display symbol, associated country or "
        "region, and monetary decimal precision."
    ),
    fields=(
        FieldDeclaration(
            name="id",
            type=FieldType.integer,
            nullable=False,
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
            description=(
                "Defines the number of decimal digits normally used for monetary "
                "values in the currency."
            ),
            has_default=True,
            default=2,
        ),
        FieldDeclaration(
            name="is_active",
            type=FieldType.boolean,
            nullable=False,
            description="Indicates whether the currency is active.",
            has_default=True,
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
    relations=(Relation(local_field="user_id", target_entity="User", target_field="id"),),
    unique_constraints=(UniqueConstraint(fields=("user_id", "code")),),
)


class Currency(Foundation, table=True):
    """Currency."""

    __tablename__ = "Currency"  # pyright: ignore[reportAssignmentType]
    declaration: ClassVar[Declaration] = _DECLARATION
    __table_args__ = table_args(_DECLARATION)

    id: int | None = column(_DECLARATION, "id")
    user_id: int = column(_DECLARATION, "user_id")
    code: str = column(_DECLARATION, "code")
    symbol: str | None = column(_DECLARATION, "symbol")
    country: str | None = column(_DECLARATION, "country")
    decimal_digits: int = column(_DECLARATION, "decimal_digits")
    is_active: bool = column(_DECLARATION, "is_active")
    description: str | None = column(_DECLARATION, "description")
