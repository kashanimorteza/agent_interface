"""The Currency Entity."""

from typing import ClassVar

from model.core._storage import mapped_field, table_arguments
from model.core.declaration import (
    Declaration,
    FieldConstraints,
    FieldDeclaration,
    FieldType,
    Relation,
    UniquenessConstraint,
    ValueGeneration,
)
from model.core.foundation import Foundation


class Currency(Foundation, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="Currency",
        description=(
            "Defines a currency that can be used by the trading system and identifies its "
            "standard code, display symbol, associated country or region, and monetary decimal "
            "precision."
        ),
        fields=(
            FieldDeclaration(
                name="id",
                type=FieldType.INTEGER,
                nullable=False,
                immutable=True,
                value_generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration(
                name="user_id",
                type=FieldType.INTEGER,
                nullable=False,
                description="Identifies the user who owns this currency.",
            ),
            FieldDeclaration(
                name="code",
                type=FieldType.STRING,
                nullable=False,
                description=(
                    "The currency's standard three-letter code, such as `USD` or `EUR`."
                ),
                constraints=FieldConstraints(size=3),
            ),
            FieldDeclaration(
                name="symbol",
                type=FieldType.STRING,
                nullable=True,
                description="The currency's display symbol, such as `$`, `€`, or `£`.",
            ),
            FieldDeclaration(
                name="country",
                type=FieldType.STRING,
                nullable=True,
                description="Identifies the country or region associated with the currency.",
            ),
            FieldDeclaration(
                name="decimal_digits",
                type=FieldType.INTEGER,
                nullable=False,
                description=(
                    "Defines the number of decimal digits normally used for monetary values in "
                    "the currency."
                ),
                default=2,
            ),
            FieldDeclaration(
                name="is_active",
                type=FieldType.BOOLEAN,
                nullable=False,
                description="Indicates whether the currency is active.",
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type=FieldType.STRING,
                nullable=True,
                description="Describes the currency.",
            ),
        ),
        relations=(Relation("user_id", "User", "id"),),
        unique_constraints=(UniquenessConstraint(("user_id", "code")),),
    )

    __tablename__ = "Currency"
    __table_args__ = table_arguments(declaration)

    id: int | None = mapped_field(declaration, "id")
    user_id: int = mapped_field(declaration, "user_id")
    code: str = mapped_field(declaration, "code")
    symbol: str | None = mapped_field(declaration, "symbol")
    country: str | None = mapped_field(declaration, "country")
    decimal_digits: int = mapped_field(declaration, "decimal_digits")
    is_active: bool = mapped_field(declaration, "is_active")
    description: str | None = mapped_field(declaration, "description")
