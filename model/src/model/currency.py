"""The Currency Domain Definition."""

from __future__ import annotations

from pydantic import Field

from .foundation import ModelBase


class Currency(ModelBase):
    """A currency usable by the trading system, with its code, symbol, and precision."""

    UNIQUE_CONSTRAINTS = (("user_id", "code"),)

    id: int | None = Field(default=None, description="Auto-incrementing primary key.")
    user_id: int = Field(..., description="Identifies the user who owns this currency.")
    code: str = Field(
        ...,
        min_length=3,
        max_length=3,
        description="The currency's standard three-letter code, such as `USD` or `EUR`.",
    )
    symbol: str | None = Field(
        default=None,
        description="The currency's display symbol, such as `$`, `€`, or `£`.",
    )
    country: str | None = Field(
        default=None, description="Identifies the country or region associated with the currency."
    )
    decimal_digits: int = Field(
        default=2,
        description="The number of decimal digits normally used for monetary values "
        "in the currency.",
    )
    is_active: bool = Field(default=True, description="Whether the currency is active.")
    description: str | None = Field(default=None, description="Describes the currency.")
