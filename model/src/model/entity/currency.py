"""The Currency Entity."""

from typing import ClassVar

from sqlmodel import Field

from model.core.base import Entity
from model.core.declaration import Declaration, FieldDeclaration, Relation
from model.core.storage import column_options, table_args

_DECLARATION = Declaration(
    name="Currency",
    description="Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.",
    fields=(
        FieldDeclaration(
            name="id",
            description=None,
            type="integer",
            nullable=False,
            immutable=True,
            value_generation="auto_increment",
        ),
        FieldDeclaration(
            name="user_id",
            description="Identifies the user who owns this currency.",
            type="integer",
            nullable=False,
        ),
        FieldDeclaration(
            name="code",
            description="The currency's standard three-letter code, such as `USD` or `EUR`.",
            type="string",
            nullable=False,
            constraints={"size": 3},
        ),
        FieldDeclaration(
            name="symbol",
            description="The currency's display symbol, such as `$`, `€`, or `£`.",
            type="string",
            nullable=True,
        ),
        FieldDeclaration(
            name="country",
            description="Identifies the country or region associated with the currency.",
            type="string",
            nullable=True,
        ),
        FieldDeclaration(
            name="decimal_digits",
            description="Defines the number of decimal digits normally used for monetary values in the currency.",
            type="integer",
            nullable=False,
            has_default=True,
            default=2,
        ),
        FieldDeclaration(
            name="is_active",
            description="Indicates whether the currency is active.",
            type="boolean",
            nullable=False,
            has_default=True,
            default=True,
        ),
        FieldDeclaration(
            name="description",
            description="Describes the currency.",
            type="string",
            nullable=True,
        ),
    ),
    primary_key="id",
    relations=(
        Relation(local_field="user_id", target_entity="User", target_field="id"),
    ),
    unique_constraints=(("user_id", "code"),),
    indexes=(),
)


class Currency(Entity, table=True):
    __table_args__ = table_args(_DECLARATION)
    declaration: ClassVar[Declaration] = _DECLARATION

    id: int | None = Field(default=None, **column_options(_DECLARATION, "id"))
    user_id: int = Field(
        description="Identifies the user who owns this currency.",
        **column_options(_DECLARATION, "user_id"),
    )
    code: str = Field(
        description="The currency's standard three-letter code, such as `USD` or `EUR`.",
        max_length=3,
        **column_options(_DECLARATION, "code"),
    )
    symbol: str | None = Field(
        default=None,
        description="The currency's display symbol, such as `$`, `€`, or `£`.",
        **column_options(_DECLARATION, "symbol"),
    )
    country: str | None = Field(
        default=None,
        description="Identifies the country or region associated with the currency.",
        **column_options(_DECLARATION, "country"),
    )
    decimal_digits: int = Field(
        default=2,
        description="Defines the number of decimal digits normally used for monetary values in the currency.",
        **column_options(_DECLARATION, "decimal_digits"),
    )
    is_active: bool = Field(
        default=True,
        description="Indicates whether the currency is active.",
        **column_options(_DECLARATION, "is_active"),
    )
    description: str | None = Field(
        default=None,
        description="Describes the currency.",
        **column_options(_DECLARATION, "description"),
    )
