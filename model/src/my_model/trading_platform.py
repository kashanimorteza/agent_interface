"""The TradingPlatform Model."""

from collections.abc import Mapping
from typing import Annotated, ClassVar

from ._base import Model
from ._spec import FieldSpec, LogicalType


class TradingPlatform(Model):
    """Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the
    system independent of any specific exchange or broker. Every trading platform implementation
    exposes the same application-facing trading functions through a dedicated class, while handling
    communication with its destination API according to that platform's own mechanism. Additional
    platform implementations can be added without changing the system's common trading interface.
    """

    logical_key: ClassVar[str] = "trading_platform"
    logical_purpose: ClassVar[str] = (
        "Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system "
        "independent of any specific exchange or broker. Every trading platform implementation exposes the "
        "same application-facing trading functions through a dedicated class, while handling communication "
        "with its destination API according to that platform's own mechanism. Additional platform "
        "implementations can be added without changing the system's common trading interface."
    )
    logical_initial_data: ClassVar[tuple[Mapping[str, object], ...]] = (
        {"name": "MetaTrader 5", "code": "metatrader_5"},
        {"name": "Binance", "code": "binance"},
    )

    id: Annotated[
        int | None,
        FieldSpec(
            type=LogicalType.integer,
            nullable=False,
            auto_increment=True,
            primary_key=True,
        ),
    ] = None
    name: Annotated[
        str,
        FieldSpec(
            type=LogicalType.string,
            nullable=False,
            unique=True,
            purpose="The platform's display name.",
        ),
    ]
    code: Annotated[
        str,
        FieldSpec(
            type=LogicalType.string,
            nullable=False,
            purpose="Identifies the implementation class the application must use for this trading platform, such as binance or metatrader_5.",
        ),
    ]
    status: Annotated[
        bool,
        FieldSpec(
            type=LogicalType.boolean,
            nullable=False,
            default=True,
            purpose="Indicates whether the platform is active.",
        ),
    ] = True
    description: Annotated[
        str | None,
        FieldSpec(
            type=LogicalType.string,
            nullable=True,
            purpose="Describes the platform.",
        ),
    ] = None
