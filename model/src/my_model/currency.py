"""The Currency Model."""

from collections.abc import Mapping
from typing import Annotated, ClassVar

from ._base import Model
from ._spec import FieldSpec, LogicalType


class Currency(Model):
    """Defines a currency that can be used by the trading system and identifies its standard code,
    display symbol, associated country or region, and monetary decimal precision.
    """

    logical_key: ClassVar[str] = "currency"
    logical_purpose: ClassVar[str] = (
        "Defines a currency that can be used by the trading system and identifies its standard code, display "
        "symbol, associated country or region, and monetary decimal precision."
    )
    logical_initial_data: ClassVar[tuple[Mapping[str, object], ...]] = (
        {"name": "US Dollar", "code": "USD", "symbol": "$", "country": "United States", "decimal_digits": 2},
        {"name": "Euro", "code": "EUR", "symbol": "€", "country": "Eurozone", "decimal_digits": 2},
        {"name": "British Pound", "code": "GBP", "symbol": "£", "country": "United Kingdom", "decimal_digits": 2},
        {"name": "Japanese Yen", "code": "JPY", "symbol": "¥", "country": "Japan", "decimal_digits": 0},
        {"name": "Swiss Franc", "code": "CHF", "symbol": "CHF", "country": "Switzerland", "decimal_digits": 2},
        {"name": "Canadian Dollar", "code": "CAD", "symbol": "C$", "country": "Canada", "decimal_digits": 2},
        {"name": "Australian Dollar", "code": "AUD", "symbol": "A$", "country": "Australia", "decimal_digits": 2},
        {
            "name": "New Zealand Dollar",
            "code": "NZD",
            "symbol": "NZ$",
            "country": "New Zealand",
            "decimal_digits": 2,
        },
    )

    id: Annotated[
        int | None,
        FieldSpec(
            type=LogicalType.integer,
            nullable=False,
            auto_increment=True,
            primary_key=True,
        ),
    ] = None
    name: Annotated[
        str,
        FieldSpec(
            type=LogicalType.string,
            nullable=False,
            unique=True,
            purpose="The currency's full name.",
        ),
    ]
    code: Annotated[
        str,
        FieldSpec(
            type=LogicalType.string,
            nullable=False,
            size=3,
            unique=True,
            purpose="The currency's standard three-letter code, such as USD or EUR.",
        ),
    ]
    symbol: Annotated[
        str | None,
        FieldSpec(
            type=LogicalType.string,
            nullable=True,
            purpose="The currency's display symbol, such as $, €, or £.",
        ),
    ] = None
    country: Annotated[
        str | None,
        FieldSpec(
            type=LogicalType.string,
            nullable=True,
            purpose="Identifies the country or region associated with the currency.",
        ),
    ] = None
    decimal_digits: Annotated[
        int,
        FieldSpec(
            type=LogicalType.integer,
            nullable=False,
            default=2,
            purpose="Defines the number of decimal digits normally used for monetary values in the currency.",
        ),
    ] = 2
    status: Annotated[
        bool,
        FieldSpec(
            type=LogicalType.boolean,
            nullable=False,
            default=True,
            purpose="Indicates whether the currency is active.",
        ),
    ] = True
    description: Annotated[
        str | None,
        FieldSpec(
            type=LogicalType.string,
            nullable=True,
            purpose="Describes the currency.",
        ),
    ] = None
