"""The Currency Domain Definition: a currency usable by the trading system."""

from typing import ClassVar

from model.foundation import DomainModel, domain_field


class Currency(DomainModel):
    """A currency, owned by a User, with its standard code, symbol, region, and monetary precision."""

    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (("user_id", "code"),)

    id: int | None = domain_field(
        default=None,
        primary_key=True,
        auto_increment=True,
        nullable=False,
        description="Identifies the currency.",
    )
    user_id: int = domain_field(
        foreign_key="User.id",
        cardinality="many_to_one",
        description="Identifies the user who owns this currency.",
    )
    code: str = domain_field(
        length=3,
        min_length=3,
        max_length=3,
        description="The currency's standard three-letter code, such as USD or EUR.",
    )
    symbol: str | None = domain_field(
        default=None, description="The currency's display symbol."
    )
    country: str | None = domain_field(
        default=None,
        description="Identifies the country or region associated with the currency.",
    )
    decimal_digits: int = domain_field(
        default=2,
        description="The number of decimal digits normally used for monetary values in the currency.",
    )
    is_active: bool = domain_field(
        default=True, description="Indicates whether the currency is active."
    )
    description: str | None = domain_field(
        default=None, description="Describes the currency."
    )
