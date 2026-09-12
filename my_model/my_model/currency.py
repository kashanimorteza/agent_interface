"""The Currency domain entity."""

from pydantic import Field

from my_model._base import BaseModel


class Currency(BaseModel):
    """A currency usable by the trading system, with its standard code,
    display symbol, associated country or region, and monetary precision.
    """

    id: int = Field(description="The currency's logical identity.")
    user_id: int = Field(description="Identifies the user who owns this currency.")
    code: str = Field(
        min_length=3,
        max_length=3,
        description="The currency's standard three-letter code.",
    )
    symbol: str | None = Field(default=None, description="The currency's display symbol.")
    country: str | None = Field(
        default=None, description="Identifies the country or region associated with the currency."
    )
    decimal_digits: int = Field(
        default=2,
        description="The number of decimal digits normally used for monetary values in the currency.",
    )
    status: bool = Field(default=True, description="Whether the currency is active.")
    description: str | None = Field(default=None, description="Describes the currency.")


INITIAL_DATA: list[dict[str, object]] = [
    {"user_id": 1, "code": "USD", "symbol": "$", "country": "United States", "decimal_digits": 2},
    {"user_id": 1, "code": "EUR", "symbol": "€", "country": "Eurozone", "decimal_digits": 2},
    {"user_id": 1, "code": "GBP", "symbol": "£", "country": "United Kingdom", "decimal_digits": 2},
    {"user_id": 1, "code": "JPY", "symbol": "¥", "country": "Japan", "decimal_digits": 0},
    {"user_id": 1, "code": "CHF", "symbol": "CHF", "country": "Switzerland", "decimal_digits": 2},
    {"user_id": 1, "code": "CAD", "symbol": "C$", "country": "Canada", "decimal_digits": 2},
    {"user_id": 1, "code": "AUD", "symbol": "A$", "country": "Australia", "decimal_digits": 2},
    {"user_id": 1, "code": "NZD", "symbol": "NZ$", "country": "New Zealand", "decimal_digits": 2},
]
