"""Currency: a currency the trading system can use."""

from __future__ import annotations

from .base import Model, field


class Currency(Model):
    """Defines a currency that can be used by the trading system and
    identifies its standard code, display symbol, associated country or
    region, and monetary decimal precision."""

    id: int | None = field("integer", primary_key=True, auto_increment=True)
    name: str = field("string", unique=True, purpose="The currency's full name.")
    code: str = field(
        "string",
        size=3,
        unique=True,
        purpose="The currency's standard three-letter code, such as USD or EUR.",
    )
    symbol: str | None = field(
        "string", nullable=True, purpose="The currency's display symbol, such as $, €, or £."
    )
    country: str | None = field(
        "string",
        nullable=True,
        purpose="Identifies the country or region associated with the currency.",
    )
    decimal_digits: int = field(
        "integer",
        default=2,
        purpose="Defines the number of decimal digits normally used for monetary values in the currency.",
    )
    status: bool = field("boolean", default=True, purpose="Indicates whether the currency is active.")
    description: str | None = field("string", nullable=True, purpose="Describes the currency.")

    initial_data = (
        {"name": "US Dollar", "code": "USD", "symbol": "$", "country": "United States", "decimal_digits": 2},
        {"name": "Euro", "code": "EUR", "symbol": "€", "country": "Eurozone", "decimal_digits": 2},
        {"name": "British Pound", "code": "GBP", "symbol": "£", "country": "United Kingdom", "decimal_digits": 2},
        {"name": "Japanese Yen", "code": "JPY", "symbol": "¥", "country": "Japan", "decimal_digits": 0},
        {"name": "Swiss Franc", "code": "CHF", "symbol": "CHF", "country": "Switzerland", "decimal_digits": 2},
        {"name": "Canadian Dollar", "code": "CAD", "symbol": "C$", "country": "Canada", "decimal_digits": 2},
        {"name": "Australian Dollar", "code": "AUD", "symbol": "A$", "country": "Australia", "decimal_digits": 2},
        {"name": "New Zealand Dollar", "code": "NZD", "symbol": "NZ$", "country": "New Zealand", "decimal_digits": 2},
    )
