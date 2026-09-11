from pydantic import Field

from ._base import BaseModel


class Currency(BaseModel):
    """A currency usable by the trading system, with its standard code, symbol, region, and precision."""

    id: int | None = Field(
        default=None, description="Generated once the Currency is persisted."
    )
    user_id: int = Field(description="Identifies the user who owns this currency.")
    code: str = Field(
        min_length=3,
        max_length=3,
        description="The currency's standard three-letter code.",
    )
    symbol: str | None = Field(
        default=None, description="The currency's display symbol."
    )
    country: str | None = Field(
        default=None,
        description="Identifies the country or region associated with the currency.",
    )
    decimal_digits: int = Field(
        default=2,
        description="The number of decimal digits normally used for monetary values in the currency.",
    )
    status: bool = Field(
        default=True, description="Indicates whether the currency is active."
    )
    description: str | None = Field(default=None, description="Describes the currency.")
