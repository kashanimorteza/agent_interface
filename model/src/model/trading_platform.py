"""The Trading Platform Domain Definition: a supported trading API standard, independent of any specific exchange or broker."""

from __future__ import annotations

from model.foundation import DomainModel, domain_field


class TradingPlatform(DomainModel):
    persistent = True

    id: int | None = domain_field(
        type="integer", nullable=False, primary_key=True, auto_increment=True
    )
    name: str = domain_field(
        type="string",
        nullable=False,
        unique=True,
        description="The platform's display name.",
    )
    code: str = domain_field(
        type="string",
        nullable=False,
        description="Identifies the implementation class the application must use for this trading platform, such as binance or metatrader_5.",
    )
    is_active: bool = domain_field(
        type="boolean",
        nullable=False,
        default=True,
        description="Indicates whether the platform is active.",
    )
    description: str | None = domain_field(
        type="string", nullable=True, description="Describes the platform."
    )
