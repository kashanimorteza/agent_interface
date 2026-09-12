"""The Currency domain entity."""

from __future__ import annotations

from pydantic import Field

from ._base import BaseModel


class Currency(BaseModel):
    """A currency usable by the trading system, identifying its standard code,
    display symbol, associated country or region, and monetary precision.
    """

    initial_data = (
        {
            "user_id": 1,
            "code": "USD",
            "symbol": "$",
            "country": "United States",
            "decimal_digits": 2,
        },
        {"user_id": 1, "code": "EUR", "symbol": "€", "country": "Eurozone", "decimal_digits": 2},
        {
            "user_id": 1,
            "code": "GBP",
            "symbol": "£",
            "country": "United Kingdom",
            "decimal_digits": 2,
        },
        {"user_id": 1, "code": "JPY", "symbol": "¥", "country": "Japan", "decimal_digits": 0},
        {
            "user_id": 1,
            "code": "CHF",
            "symbol": "CHF",
            "country": "Switzerland",
            "decimal_digits": 2,
        },
        {"user_id": 1, "code": "CAD", "symbol": "C$", "country": "Canada", "decimal_digits": 2},
        {"user_id": 1, "code": "AUD", "symbol": "A$", "country": "Australia", "decimal_digits": 2},
        {
            "user_id": 1,
            "code": "NZD",
            "symbol": "NZ$",
            "country": "New Zealand",
            "decimal_digits": 2,
        },
    )

    id: int | None = Field(
        default=None, description="System-generated identity, absent until persisted."
    )
    user_id: int = Field(description="Identifies the user who owns this currency.")
    code: str = Field(
        min_length=3, max_length=3, description="The currency's standard three-letter code."
    )
    symbol: str | None = Field(default=None, description="The currency's display symbol.")
    country: str | None = Field(
        default=None, description="The country or region associated with the currency."
    )
    decimal_digits: int = Field(
        default=2, ge=0, description="Decimal digits normally used for monetary values."
    )
    status: bool = Field(default=True, description="Whether the currency is active.")
    description: str | None = Field(default=None, description="Describes the currency.")
