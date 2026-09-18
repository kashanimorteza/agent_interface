"""The Trading Platform Domain Definition: a supported trading API standard."""

from model.foundation import DomainModel, domain_field


class TradingPlatform(DomainModel):
    """A supported trading platform, such as MetaTrader 5 or Binance."""

    id: int | None = domain_field(
        default=None,
        primary_key=True,
        auto_increment=True,
        nullable=False,
        description="Identifies the trading platform.",
    )
    name: str = domain_field(unique=True, description="The platform's display name.")
    code: str = domain_field(
        description="Identifies the implementation class the application must use for this trading platform."
    )
    is_active: bool = domain_field(
        default=True, description="Indicates whether the platform is active."
    )
    description: str | None = domain_field(
        default=None, description="Describes the platform."
    )
