"""The Trading Platform domain entity: a supported trading API standard."""

from pydantic import Field

from my_model._base import BaseModel


class TradingPlatform(BaseModel):
    """A supported trading API standard, such as MetaTrader 5 or Binance.

    Every trading platform implementation exposes the same application-facing
    trading functions through a dedicated class, while handling communication
    with its destination API according to that platform's own mechanism, so
    additional platform implementations can be added without changing the
    system's common trading interface.
    """

    id: int = Field(description="The trading platform's logical identity.")
    name: str = Field(description="The platform's display name.")
    code: str = Field(
        description=(
            "Identifies the implementation class the application must use "
            "for this trading platform."
        )
    )
    status: bool = Field(default=True, description="Whether the platform is active.")
    description: str | None = Field(default=None, description="Describes the platform.")


INITIAL_DATA: list[dict[str, object]] = [
    {"name": "MetaTrader 5", "code": "metatrader_5"},
    {"name": "Binance", "code": "binance"},
]
