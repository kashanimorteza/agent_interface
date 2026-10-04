"""The Currency Entity."""

from sqlmodel import Field

from model.core._base import Entity
from model.core._defaults import (
    activity_declaration,
    activity_field,
    identity_declaration,
    identity_field,
)
from model.core._storage import table_arguments
from model.core.declaration import Declaration, FieldDeclaration, RelationDeclaration


class Currency(Entity, table=True):
    """The Currency Entity."""

    __tablename__ = "Currency"  # pyright: ignore[reportAssignmentType]
    __table_args__ = table_arguments(
        ("user_id", "code"),
    )

    declaration = Declaration(
        name="Currency",
        description="Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.",
        fields=(
            identity_declaration(),
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
                constraints=(("size", 3),),
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
                default=2,
            ),
            activity_declaration("Indicates whether the currency is active."),
            FieldDeclaration(
                name="description",
                description="Describes the currency.",
                type="string",
                nullable=True,
            ),
        ),
        primary_key="id",
        relations=(
            RelationDeclaration(
                local_field="user_id", target_entity="User", target_field="id"
            ),
        ),
        unique_constraints=(("user_id", "code"),),
    )

    id: int | None = identity_field()
    user_id: int = Field(
        foreign_key="User.id", description="Identifies the user who owns this currency."
    )
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
    is_active: bool = activity_field("Indicates whether the currency is active.")
    description: str | None = Field(default=None, description="Describes the currency.")
