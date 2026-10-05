from typing import ClassVar

from model.core.base import Entity
from model.core.columns import column, table_arguments
from model.core.declaration import (
    Declaration,
    FieldConstraints,
    FieldDeclaration,
    FieldType,
    RelationDeclaration,
    UniqueConstraintDeclaration,
    activity,
    identity,
)

_DECLARATION = Declaration(
    name="Currency",
    description="Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.",
    fields=(
        identity(),
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
            constraints=FieldConstraints(size=3),
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
            default=2,
        ),
        activity("Indicates whether the currency is active."),
        FieldDeclaration(
            name="description",
            description="Describes the currency.",
            type=FieldType.STRING,
            nullable=True,
        ),
    ),
    primary_key="id",
    relations=(RelationDeclaration("user_id", "User", "id"),),
    unique_constraints=(
        UniqueConstraintDeclaration(
            (
                "user_id",
                "code",
            )
        ),
    ),
)


class Currency(Entity, table=True):
    __table_args__ = table_arguments(_DECLARATION)
    declaration: ClassVar[Declaration] = _DECLARATION

    id: int | None = column(_DECLARATION, "id")
    user_id: int = column(_DECLARATION, "user_id")
    code: str = column(_DECLARATION, "code")
    symbol: str | None = column(_DECLARATION, "symbol")
    country: str | None = column(_DECLARATION, "country")
    decimal_digits: int = column(_DECLARATION, "decimal_digits")
    is_active: bool = column(_DECLARATION, "is_active")
    description: str | None = column(_DECLARATION, "description")
