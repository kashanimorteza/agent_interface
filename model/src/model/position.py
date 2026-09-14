"""The Position Domain Definition."""

from __future__ import annotations

from decimal import Decimal
from typing import ClassVar

from .foundation import (
    ModelBase,
    TimezoneAwareDatetime,
    UniqueConstraints,
    identity_field,
)


class Position(ModelBase):
    """The complete information for a position the system has created, executed or pending."""

    id: int = identity_field()
    user_id: int
    name: str
    trading_platform_id: int
    broker_id: int
    account_id: int
    trailing_group_id: int
    partial_group_id: int
    action_group_id: int
    action_id: int
    date: TimezoneAwareDatetime
    volume: Decimal
    profit: Decimal = Decimal(0)
    is_executed: bool = False
    order_type: str
    base_tp: Decimal
    base_sl: Decimal
    real_tp: Decimal
    real_sl: Decimal
    status: bool = True
    description: str | None = None

    unique_constraints: ClassVar[UniqueConstraints] = (("name",),)
