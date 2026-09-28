from typing import ClassVar

from sqlmodel import Field

from ..core.base import Entity
from ..core.declaration import Declaration, FieldDeclaration, Relation, ValueGeneration
from ..core.logical_type import LogicalType


class Currency(Entity, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="Currency",
        description="Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.",
        fields=(
            FieldDeclaration(
                name="id",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=False,
                default=None,
                immutable=True,
                value_generation=ValueGeneration.AUTO_INCREMENT,
            ),
            FieldDeclaration(
                name="user_id",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="Identifies the user who owns this currency.",
            ),
            FieldDeclaration(
                name="code",
                type=LogicalType.STRING,
                nullable=False,
                has_default=False,
                default=None,
                immutable=False,
                description="The currency's standard three-letter code, such as `USD` or `EUR`.",
                length=3,
            ),
            FieldDeclaration(
                name="symbol",
                type=LogicalType.STRING,
                nullable=True,
                has_default=False,
                default=None,
                immutable=False,
                description="The currency's display symbol, such as `$`, `€`, or `£`.",
            ),
            FieldDeclaration(
                name="country",
                type=LogicalType.STRING,
                nullable=True,
                has_default=False,
                default=None,
                immutable=False,
                description="Identifies the country or region associated with the currency.",
            ),
            FieldDeclaration(
                name="decimal_digits",
                type=LogicalType.INTEGER,
                nullable=False,
                has_default=True,
                default=2,
                immutable=False,
                description="Defines the number of decimal digits normally used for monetary values in the currency.",
            ),
            FieldDeclaration(
                name="is_active",
                type=LogicalType.BOOLEAN,
                nullable=False,
                has_default=True,
                default=True,
                immutable=False,
                description="Indicates whether the currency is active.",
            ),
            FieldDeclaration(
                name="description",
                type=LogicalType.STRING,
                nullable=True,
                has_default=False,
                default=None,
                immutable=False,
                description="Describes the currency.",
            ),
        ),
        primary_key="id",
        relations=(Relation(local_field="user_id", target_entity="User", target_field="id"),),
        unique_constraints=(("user_id", "code"),),
        indexes=(),
    )

    id: int | None = Field(default=None, primary_key=True)
    user_id: int
    code: str = Field(max_length=3)
    symbol: str | None = None
    country: str | None = None
    decimal_digits: int = 2
    is_active: bool = True
    description: str | None = None
