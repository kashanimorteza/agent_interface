"""The Currency Entity."""

from typing import ClassVar

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from my_model.model_declaration import (
    FieldDeclaration,
    Model_Declaration,
    ReferenceDeclaration,
)
from my_model.model_foundation import Model_Foundation


class Currency(Model_Foundation, table=True):
    """A currency usable by the trading system, with its standard code, symbol, region, and decimal precision."""

    declaration: ClassVar[Model_Declaration] = Model_Declaration(
        entity="Currency",
        purpose="A currency usable by the trading system, with its standard code, symbol, region, and decimal precision.",
        fields=(
            FieldDeclaration(
                name="id",
                type="integer",
                nullable=False,
                value_generation="auto_increment",
            ),
            FieldDeclaration(
                name="user_id",
                type="integer",
                nullable=False,
                purpose="Identifies the user who owns this currency.",
            ),
            FieldDeclaration(
                name="code",
                type="string",
                nullable=False,
                purpose="The currency's standard three-letter code, such as USD or EUR.",
                length=3,
            ),
            FieldDeclaration(
                name="symbol",
                type="string",
                nullable=True,
                purpose="The currency's display symbol.",
            ),
            FieldDeclaration(
                name="country",
                type="string",
                nullable=True,
                purpose="The country or region associated with the currency.",
            ),
            FieldDeclaration(
                name="decimal_digits",
                type="integer",
                nullable=False,
                purpose="The number of decimal digits normally used for monetary values in the currency.",
                has_default=True,
                default=2,
            ),
            FieldDeclaration(
                name="is_active",
                type="boolean",
                nullable=False,
                purpose="Indicates whether the currency is active.",
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type="string",
                nullable=True,
                purpose="Describes the currency.",
            ),
        ),
        references=(ReferenceDeclaration(field="user_id", entity="User"),),
        unique_constraints=(("user_id", "code"),),
    )
    __table_args__ = (UniqueConstraint("user_id", "code"),)

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    code: str = Field(max_length=3)
    symbol: str | None = None
    country: str | None = None
    decimal_digits: int = 2
    is_active: bool = True
    description: str | None = None
