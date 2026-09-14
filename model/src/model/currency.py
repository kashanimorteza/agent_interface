"""The Currency Domain Definition (Target: Model > Currency)."""

from __future__ import annotations

import pydantic

from model.foundation import (
    ModelFoundation,
    description_field,
    id_field,
    is_active_field,
)


class Currency(ModelFoundation):
    """A currency usable by the trading system, identifying its standard code, display symbol,
    associated country or region, and monetary decimal precision."""

    id: int = id_field()
    user_id: int = pydantic.Field(
        description="Identifies the user who owns this currency."
    )
    code: str = pydantic.Field(
        min_length=3,
        max_length=3,
        description="The currency's standard three-letter code, such as `USD` or `EUR`.",
    )
    symbol: str | None = pydantic.Field(
        default=None,
        description="The currency's display symbol, such as `$`, `€`, or `£`.",
    )
    country: str | None = pydantic.Field(
        default=None,
        description="Identifies the country or region associated with the currency.",
    )
    decimal_digits: int = pydantic.Field(
        default=2,
        description="Defines the number of decimal digits normally used for monetary values in the currency.",
    )
    is_active: bool = is_active_field("Indicates whether the currency is active.")
    description: str | None = description_field("Describes the currency.")
