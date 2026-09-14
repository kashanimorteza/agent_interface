"""The Trailing Rule Domain Definition."""

from __future__ import annotations

from decimal import Decimal
from typing import ClassVar

from .foundation import ModelBase, UniqueConstraints, identity_field


class TrailingRule(ModelBase):
    """One rule within a Trailing Group telling the system when and how to manage Take Profit and Stop Loss."""

    id: int = identity_field()
    name: str
    trailing_group_id: int
    trigger_percentage: Decimal
    take_profit_adjustment: Decimal | None = None
    stop_loss_adjustment: Decimal | None = None
    status: bool = True
    description: str | None = None

    unique_constraints: ClassVar[UniqueConstraints] = (
        ("name",),
        ("trailing_group_id", "trigger_percentage"),
    )
