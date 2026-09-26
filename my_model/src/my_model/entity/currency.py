"""Currency Entity."""

from typing import ClassVar

from sqlmodel import Field, UniqueConstraint

from my_model.model_declaration import (
    FieldDeclaration,
    LogicalType,
    ModelDeclaration,
    Reference,
    RelationshipKind,
    UniquenessConstraint,
    ValueGeneration,
)
from my_model.model_foundation import ModelFoundation


class Currency(ModelFoundation, table=True):
    """Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision."""

    declaration: ClassVar[ModelDeclaration] = ModelDeclaration(
        entity="Currency",
        purpose="Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.",
        fields=(
            FieldDeclaration(
                "id",
                LogicalType.INTEGER,
                generation=ValueGeneration.AUTO_INCREMENT,
                purpose="",
            ),
            FieldDeclaration(
                "user_id",
                LogicalType.INTEGER,
                purpose="Identifies the user who owns this currency",
            ),
            FieldDeclaration(
                "code",
                LogicalType.STRING,
                size=3,
                purpose="The currency's standard three-letter code, such as `USD` or `EUR`",
            ),
            FieldDeclaration(
                "symbol",
                LogicalType.STRING,
                nullable=True,
                purpose="The currency's display symbol, such as `$`, `€`, or `£`",
            ),
            FieldDeclaration(
                "country",
                LogicalType.STRING,
                nullable=True,
                purpose="Identifies the country or region associated with the currency",
            ),
            FieldDeclaration(
                "decimal_digits",
                LogicalType.INTEGER,
                has_default=True,
                default=2,
                purpose="Defines the number of decimal digits normally used for monetary values in the currency",
            ),
            FieldDeclaration(
                "is_active",
                LogicalType.BOOLEAN,
                has_default=True,
                default=True,
                purpose="Indicates whether the currency is active",
            ),
            FieldDeclaration(
                "description",
                LogicalType.STRING,
                nullable=True,
                purpose="Describes the currency",
            ),
        ),
        references=(Reference("user_id", "User", "id", RelationshipKind.BELONGS_TO),),
        unique_constraints=(
            UniquenessConstraint(
                (
                    "user_id",
                    "code",
                )
            ),
        ),
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
