"""Trading Platform Entity."""

from model.declaration import Declaration
from model.foundation import Foundation


class TradingPlatform(Foundation, table=True):
    """Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface."""

    id: int | None = Declaration.identity()
    name: str = Declaration.field(
        unique=True, description="The platform's display name."
    )
    code: str = Declaration.field(
        description="Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`."
    )
    is_active: bool = Declaration.field(
        default=True, description="Indicates whether the platform is active."
    )
    description: str | None = Declaration.field(
        nullable=True, description="Describes the platform."
    )
