"""The Trading Platform domain Model: a supported trading API standard."""

from pydantic import Field

from ._base import BaseModel


class TradingPlatform(BaseModel):
    """A supported trading API standard, such as MetaTrader 5 or Binance.

    Keeps the system independent of any specific exchange or broker. Every trading
    platform implementation exposes the same application-facing trading functions
    through a dedicated class, while handling communication with its destination
    API according to that platform's own mechanism.
    """

    id: int | None = Field(default=None, description="The trading platform's generated identity.")
    name: str = Field(description="The platform's display name.")
    code: str = Field(
        description=(
            "Identifies the implementation class the application must use for this "
            "trading platform, such as `binance` or `metatrader_5`."
        )
    )
    status: bool = Field(default=True, description="Indicates whether the platform is active.")
    description: str | None = Field(default=None, description="Describes the platform.")


INITIAL_DATA: list[dict[str, object]] = [
    {"name": "MetaTrader 5", "code": "metatrader_5"},
    {"name": "Binance", "code": "binance"},
]
