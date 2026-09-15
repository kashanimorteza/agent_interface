"""The Currency Domain Definition."""

from __future__ import annotations

from typing import ClassVar

from model.foundation import ModelBase, persistence_field


class Currency(ModelBase):
    """A currency usable by the trading system, owned by one user.

    Identifies its standard code, display symbol, associated country or
    region, and monetary decimal precision.
    """

    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (("user_id", "code"),)

    id: int = persistence_field(
        primary_key=True,
        auto_increment=True,
        description="Primary identity of the currency.",
    )
    user_id: int = persistence_field(
        foreign_key="user.id", description="Identifies the user who owns this currency."
    )
    code: str = persistence_field(
        min_length=3,
        max_length=3,
        description="The currency's standard three-letter code, such as USD or EUR.",
    )
    symbol: str | None = persistence_field(
        default=None,
        description="The currency's display symbol, such as $, EUR, or GBP.",
    )
    country: str | None = persistence_field(
        default=None,
        description="Identifies the country or region associated with the currency.",
    )
    decimal_digits: int = persistence_field(
        default=2,
        description="The number of decimal digits normally used for monetary values in the currency.",
    )
    is_active: bool = persistence_field(
        default=True, description="Indicates whether the currency is active."
    )
    description: str | None = persistence_field(
        default=None, description="Describes the currency."
    )
