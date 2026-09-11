"""A currency usable by the trading system."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from ._base import DomainModel


class Currency(DomainModel):
    """A currency owned by one User, identified by its standard three-letter code."""

    unique_together = (("user_id", "code"),)

    id: int | None = Field(default=None, description="Primary key, auto-incremented.")
    user_id: int = Field(description="Identifies the user who owns this currency.")
    code: str = Field(max_length=3, description="The currency's standard three-letter code, such as USD or EUR.")
    symbol: str | None = Field(default=None, description="The currency's display symbol, such as $, €, or £.")
    country: str | None = Field(default=None, description="Identifies the country or region associated with the currency.")
    decimal_digits: int = Field(
        default=2, description="The number of decimal digits normally used for monetary values in the currency."
    )
    status: bool = Field(default=True, description="Indicates whether the currency is active.")
    description: str | None = Field(default=None, description="Describes the currency.")


INITIAL_DATA: tuple[dict[str, Any], ...] = (
    {"user_id": 1, "code": "USD", "symbol": "$", "country": "United States", "decimal_digits": 2},
    {"user_id": 1, "code": "EUR", "symbol": "€", "country": "Eurozone", "decimal_digits": 2},
    {"user_id": 1, "code": "GBP", "symbol": "£", "country": "United Kingdom", "decimal_digits": 2},
    {"user_id": 1, "code": "JPY", "symbol": "¥", "country": "Japan", "decimal_digits": 0},
    {"user_id": 1, "code": "CHF", "symbol": "CHF", "country": "Switzerland", "decimal_digits": 2},
    {"user_id": 1, "code": "CAD", "symbol": "C$", "country": "Canada", "decimal_digits": 2},
    {"user_id": 1, "code": "AUD", "symbol": "A$", "country": "Australia", "decimal_digits": 2},
    {"user_id": 1, "code": "NZD", "symbol": "NZ$", "country": "New Zealand", "decimal_digits": 2},
)
