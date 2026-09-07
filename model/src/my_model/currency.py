"""The Currency Model."""

from pydantic import Field

from ._base import Model


class Currency(Model):
    """Defines a currency that can be used by the trading system and identifies its standard code,
    display symbol, associated country or region, and monetary decimal precision.
    """

    id: int | None = Field(default=None, description="Assigned by persistence on create; absent until then.")
    name: str = Field(description="The currency's full name. Unique.")
    code: str = Field(
        description="The currency's standard three-letter code, such as USD or EUR. Unique. At most 3 characters.",
        max_length=3,
    )
    symbol: str | None = Field(default=None, description="The currency's display symbol, such as $, €, or £.")
    country: str | None = Field(
        default=None,
        description="Identifies the country or region associated with the currency.",
    )
    decimal_digits: int = Field(
        default=2,
        description="Defines the number of decimal digits normally used for monetary values in the currency.",
    )
    status: bool = Field(default=True, description="Indicates whether the currency is active.")
    description: str | None = Field(default=None, description="Describes the currency.")
