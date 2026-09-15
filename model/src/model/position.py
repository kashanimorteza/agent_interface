"""Domain Definition for Position."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import Field, field_validator

from model.foundation import DomainModel, ForeignKey


class Position(DomainModel):
    """Stores the complete information for every position created by the system."""

    __primary_key__ = ("id",)
    __auto_increment__ = ("id",)
    __unique__ = ("name",)
    __unique_sets__ = ()
    __foreign_keys__ = {
        "user_id": ForeignKey(target="User", field="id", cardinality="many_to_one"),
        "trading_platform_id": ForeignKey(
            target="TradingPlatform", field="id", cardinality="many_to_one"
        ),
        "broker_id": ForeignKey(target="Broker", field="id", cardinality="many_to_one"),
        "account_id": ForeignKey(target="Account", field="id", cardinality="many_to_one"),
        "trailing_group_id": ForeignKey(
            target="TrailingGroup", field="id", cardinality="many_to_one"
        ),
        "partial_group_id": ForeignKey(
            target="PartialGroup", field="id", cardinality="many_to_one"
        ),
        "action_group_id": ForeignKey(target="ActionGroup", field="id", cardinality="many_to_one"),
        "action_id": ForeignKey(target="Action", field="id", cardinality="many_to_one"),
    }
    __credentials__ = {}

    id: int = Field(...)
    user_id: int = Field(...)
    name: str = Field(...)
    trading_platform_id: int = Field(...)
    broker_id: int = Field(...)
    account_id: int = Field(...)
    trailing_group_id: int = Field(...)
    partial_group_id: int = Field(...)
    action_group_id: int = Field(...)
    action_id: int = Field(...)
    date: datetime = Field(...)
    volume: Decimal = Field(...)
    profit: Decimal = Field(default=Decimal(0))
    is_executed: bool = Field(default=False)
    order_type: str = Field(...)
    base_tp: Decimal = Field(...)
    base_sl: Decimal = Field(...)
    real_tp: Decimal = Field(...)
    real_sl: Decimal = Field(...)
    is_active: bool = Field(default=True)
    description: str | None = Field(default=None)

    @field_validator("date")
    @classmethod
    def _date_must_be_timezone_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("date must be timezone-aware")
        return value
