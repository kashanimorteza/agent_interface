"""Currency Entity."""

from typing import ClassVar

from model.core import _storage as storage
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
    declaration: ClassVar[Declaration] = Declaration(
        name="Currency",
        description="Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.",
        primary_key="id",
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
        relations=(
            Relation(local_field="user_id", target_entity="User", target_field="id"),
        ),
        unique_constraints=(("user_id", "code"),),
    )
    __tablename__ = "Currency"
    __table_args__ = storage.table_args(declaration)

    id: int | None = storage.field(declaration, "id")
    user_id: int = storage.field(declaration, "user_id")
    code: str = storage.field(declaration, "code")
    symbol: str | None = storage.field(declaration, "symbol")
    country: str | None = storage.field(declaration, "country")
    decimal_digits: int = storage.field(declaration, "decimal_digits")
    is_active: bool = storage.field(declaration, "is_active")
    description: str | None = storage.field(declaration, "description")
