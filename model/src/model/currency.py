"""The Currency Domain Definition: a currency usable by the trading system, with its standard code, symbol, region, and monetary precision."""

from __future__ import annotations

from typing import ClassVar

from model.foundation import DomainModel, ForeignKeyDeclaration, domain_field


class Currency(DomainModel):
    persistent = True
    unique_sets: ClassVar[list[list[str]]] = [["user_id", "code"]]

    id: int | None = domain_field(
        type="integer", nullable=False, primary_key=True, auto_increment=True
    )
    user_id: int = domain_field(
        type="integer",
        nullable=False,
        foreign_key=ForeignKeyDeclaration(
            references="User", field="id", cardinality="many_to_one", optional=False
        ),
        description="Identifies the user who owns this currency.",
    )
    code: str = domain_field(
        type="string",
        nullable=False,
        length=3,
        description="The currency's standard three-letter code, such as USD or EUR.",
    )
    symbol: str | None = domain_field(
        type="string",
        nullable=True,
        description="The currency's display symbol, such as $, €, or £.",
    )
    country: str | None = domain_field(
        type="string",
        nullable=True,
        description="Identifies the country or region associated with the currency.",
    )
    decimal_digits: int = domain_field(
        type="integer",
        nullable=False,
        default=2,
        description="Defines the number of decimal digits normally used for monetary values in the currency.",
    )
    is_active: bool = domain_field(
        type="boolean",
        nullable=False,
        default=True,
        description="Indicates whether the currency is active.",
    )
    description: str | None = domain_field(
        type="string", nullable=True, description="Describes the currency."
    )
