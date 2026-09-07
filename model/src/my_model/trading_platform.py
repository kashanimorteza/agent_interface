"""The TradingPlatform Model."""

from pydantic import Field

from ._base import Model


class TradingPlatform(Model):
    """Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the
    system independent of any specific exchange or broker. Every trading platform implementation
    exposes the same application-facing trading functions through a dedicated class, while handling
    communication with its destination API according to that platform's own mechanism. Additional
    platform implementations can be added without changing the system's common trading interface.
    """

    id: int | None = Field(default=None, description="Assigned by persistence on create; absent until then.")
    name: str = Field(description="The platform's display name. Unique.")
    code: str = Field(
        description="Identifies the implementation class the application must use for this trading platform, such as binance or metatrader_5.",
    )
    status: bool = Field(default=True, description="Indicates whether the platform is active.")
    description: str | None = Field(default=None, description="Describes the platform.")
