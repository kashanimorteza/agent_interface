"""The Trading Platform Domain Definition."""

from typing import Annotated

from model.foundation import (
    Declare,
    ModelFoundation,
)

__all__ = ["TradingPlatform"]


class TradingPlatform(
    ModelFoundation,
    description="Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.",
    persistent="persistent",
):
    id: Annotated[
        int,
        Declare(
            description="The unique identity of the trading platform.",
            logical_type="integer",
            identity=True,
            generated=True,
        ),
    ]
    name: Annotated[
        str,
        Declare(
            description="The platform's display name.",
            logical_type="string",
            unique=True,
        ),
    ]
    code: Annotated[
        str,
        Declare(
            description="Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`.",
            logical_type="string",
        ),
    ]
    is_active: Annotated[
        bool,
        Declare(
            description="Indicates whether the platform is active.",
            logical_type="boolean",
        ),
    ] = True
    description: Annotated[
        str | None,
        Declare(description="Describes the platform.", logical_type="string"),
    ]
