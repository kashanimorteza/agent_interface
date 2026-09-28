"""The Currency Entity."""

from typing import ClassVar

from sqlmodel import Field
from sqlmodel import UniqueConstraint as TableUniqueConstraint

from model.core.base import Entity
from model.core.declaration import (
    Constraints,
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    UniqueConstraint,
    ValueGeneration,
)


class Currency(Entity, table=True):
    """The Currency Entity."""

    declaration: ClassVar[Declaration] = Declaration(
        name="Currency",
        description="Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.",
        fields=(
            FieldDeclaration(
                name="id",
                type=FieldType.INTEGER,
                nullable=False,
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
                description="The currency's standard three-letter code, such as `USD` or `EUR`.",
                constraints=Constraints(length=3),
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
                description="Defines the number of decimal digits normally used for monetary values in the currency.",
                has_default=True,
                default=2,
            ),
            FieldDeclaration(
                name="is_active",
                type=FieldType.BOOLEAN,
                nullable=False,
                description="Indicates whether the currency is active.",
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type=FieldType.STRING,
                nullable=True,
                description="Describes the currency.",
            ),
        ),
        primary_key="id",
        relations=(
            Relation(local_field="user_id", target_entity="User", target_field="id"),
        ),
        unique_constraints=(UniqueConstraint(fields=("user_id", "code")),),
    )

    __table_args__ = (TableUniqueConstraint("user_id", "code"),)

    id: int | None = Field(default=None, primary_key=True)
    user_id: int
    code: str = Field(max_length=3)
    symbol: str | None = None
    country: str | None = None
    decimal_digits: int = 2
    is_active: bool = True
    description: str | None = None
