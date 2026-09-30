"""The Currency Entity."""

from typing import ClassVar

from sqlmodel import Field

from model.core._entity import Entity
from model.core._fields import activity, identity
from model.core.declaration import Declaration as EntityDeclaration
from model.core.declaration import FieldDeclaration, Relation


class Currency(Entity):
    Declaration: ClassVar[EntityDeclaration] = EntityDeclaration(
        name="Currency",
        description=(
            "Defines a currency that can be used by the trading "
            "system and identifies its standard code, display "
            "symbol, associated country or region, and monetary "
            "decimal precision."
        ),
        fields=(
            identity(),
            FieldDeclaration(
                "user_id",
                "integer",
                nullable=False,
                description="Identifies the user who owns this currency.",
            ),
            FieldDeclaration(
                "code",
                "string",
                nullable=False,
                description=(
                    "The currency's standard three-letter code, such as `USD` or `EUR`."
                ),
                constraints={"size": 3},
            ),
            FieldDeclaration(
                "symbol",
                "string",
                nullable=True,
                description=(
                    "The currency's display symbol, such as `$`, `€`, or `£`."
                ),
            ),
            FieldDeclaration(
                "country",
                "string",
                nullable=True,
                description=(
                    "Identifies the country or region associated with the currency."
                ),
            ),
            FieldDeclaration(
                "decimal_digits",
                "integer",
                nullable=False,
                description=(
                    "Defines the number of decimal digits normally used "
                    "for monetary values in the currency."
                ),
                has_default=True,
                default=2,
            ),
            activity("Indicates whether the currency is active."),
            FieldDeclaration(
                "description",
                "string",
                nullable=True,
                description="Describes the currency.",
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
