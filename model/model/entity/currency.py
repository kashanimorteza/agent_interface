from typing import ClassVar

from sqlalchemy import Identity, UniqueConstraint
from sqlmodel import Field

from model.core._base import EntityBase
from model.core.declaration import Declaration, FieldDeclaration, Relation


class Currency(EntityBase, table=True):
    __table_args__ = (
        UniqueConstraint("user_id", "code"),
        {"sqlite_autoincrement": True},
    )
    declaration: ClassVar[Declaration] = Declaration(
        "Currency",
        "Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.",
        (
            FieldDeclaration("id", None, "integer", False, immutable=True, value_generation="auto_increment"),
            FieldDeclaration("user_id", "Identifies the user who owns this currency.", "integer", False),
            FieldDeclaration(
                "code",
                "The currency's standard three-letter code, such as `USD` or `EUR`.",
                "string",
                False,
                constraints={"size": 3},
            ),
            FieldDeclaration("symbol", "The currency's display symbol, such as `$`, `€`, or `£`.", "string", True),
            FieldDeclaration(
                "country", "Identifies the country or region associated with the currency.", "string", True
            ),
            FieldDeclaration(
                "decimal_digits",
                "Defines the number of decimal digits normally used for monetary values in the currency.",
                "integer",
                False,
                has_default=True,
                default=2,
            ),
            FieldDeclaration(
                "is_active",
                "Indicates whether the currency is active.",
                "boolean",
                False,
                has_default=True,
                default=True,
            ),
            FieldDeclaration("description", "Describes the currency.", "string", True),
        ),
        "id",
        relations=(Relation("user_id", "User", "id"),),
        unique_constraints=(
            (
                "user_id",
                "code",
            ),
        ),
    )
    id: int | None = Field(default=None, primary_key=True, sa_column_args=[Identity()])
    user_id: int = Field(foreign_key="User.id", description="Identifies the user who owns this currency.")
    code: str = Field(max_length=3, description="The currency's standard three-letter code, such as `USD` or `EUR`.")
    symbol: str | None = Field(default=None, description="The currency's display symbol, such as `$`, `€`, or `£`.")
    country: str | None = Field(
        default=None, description="Identifies the country or region associated with the currency."
    )
    decimal_digits: int = Field(
        default=2, description="Defines the number of decimal digits normally used for monetary values in the currency."
    )
    is_active: bool = Field(default=True, description="Indicates whether the currency is active.")
    description: str | None = Field(default=None, description="Describes the currency.")
