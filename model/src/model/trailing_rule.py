"""Domain Definition for Trailing Rule."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from model.foundation import DomainModel, ForeignKey


class TrailingRule(DomainModel):
    """Defines an individual rule within a Trailing Group that tells the system when and
    how to manage Take Profit and Stop Loss.
    """

    __primary_key__ = ("id",)
    __auto_increment__ = ("id",)
    __unique__ = ("name",)
    __unique_sets__ = (("trailing_group_id", "trigger_percentage"),)
    __foreign_keys__ = {
        "trailing_group_id": ForeignKey(
            target="TrailingGroup", field="id", cardinality="many_to_one"
        )
    }
    __credentials__ = {}

    id: int = Field(...)
    name: str = Field(...)
    trailing_group_id: int = Field(...)
    trigger_percentage: Decimal = Field(...)
    take_profit_adjustment: Decimal | None = Field(default=None)
    stop_loss_adjustment: Decimal | None = Field(default=None)
    is_active: bool = Field(default=True)
    description: str | None = Field(default=None)
