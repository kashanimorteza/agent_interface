"""The Position Domain Definition: the complete information for every position the system creates."""

from datetime import UTC
from decimal import Decimal
from typing import Annotated

from pydantic import AfterValidator, AwareDatetime

from model.foundation import DomainModel, domain_field


def _to_utc(value: AwareDatetime) -> AwareDatetime:
    """Normalize an absolute instant to Model's canonical timezone (UTC)."""

    return value.astimezone(UTC)


class Position(DomainModel):
    """Tracks a position that has been opened, or is still pending execution."""

    id: int | None = domain_field(
        default=None,
        primary_key=True,
        auto_increment=True,
        nullable=False,
        description="Identifies the position.",
    )
    user_id: int = domain_field(
        foreign_key="User.id",
        cardinality="many_to_one",
        description="Identifies the user who owns the position.",
    )
    name: str = domain_field(unique=True, description="The position's display name.")
    trading_platform_id: int = domain_field(
        foreign_key="TradingPlatform.id",
        cardinality="many_to_one",
        description="Identifies the trading platform used to execute the position.",
    )
    broker_id: int = domain_field(
        foreign_key="Broker.id",
        cardinality="many_to_one",
        description="Identifies the broker through which the position is executed.",
    )
    account_id: int = domain_field(
        foreign_key="Account.id",
        cardinality="many_to_one",
        description="Identifies the trading account used for the position.",
    )
    trailing_group_id: int = domain_field(
        foreign_key="TrailingGroup.id",
        cardinality="many_to_one",
        description="Identifies the Trailing Group applied to the position.",
    )
    partial_group_id: int = domain_field(
        foreign_key="PartialGroup.id",
        cardinality="many_to_one",
        description="Identifies the Partial Group applied to the position.",
    )
    action_group_id: int = domain_field(
        foreign_key="ActionGroup.id",
        cardinality="many_to_one",
        description="Identifies the Action Group associated with the position.",
    )
    action_id: int = domain_field(
        foreign_key="Action.id",
        cardinality="many_to_one",
        description="Identifies the action from which the position is created.",
    )
    date: Annotated[AwareDatetime, AfterValidator(_to_utc)] = domain_field(
        description="Stores the position's date and time (timezone-aware, normalized to UTC)."
    )
    volume: Decimal = domain_field(description="Stores the position's trading volume.")
    profit: Decimal = domain_field(
        default=Decimal(0), description="Stores the position's current profit or loss."
    )
    is_executed: bool = domain_field(
        default=False, description="Indicates whether the position has been executed."
    )
    order_type: str = domain_field(description="Stores the position's order type.")
    base_tp: Decimal = domain_field(
        description="Stores the position's initial Take Profit value."
    )
    base_sl: Decimal = domain_field(
        description="Stores the position's initial Stop Loss value."
    )
    real_tp: Decimal = domain_field(
        description="Stores the position's current Take Profit value."
    )
    real_sl: Decimal = domain_field(
        description="Stores the position's current Stop Loss value."
    )
    is_active: bool = domain_field(
        default=True, description="Indicates whether the position is active."
    )
    description: str | None = domain_field(
        default=None, description="Describes the position."
    )
