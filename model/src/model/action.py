"""Domain Definition for Action."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from model.foundation import DomainModel, ForeignKey


class Action(DomainModel):
    """Defines how a position must be opened."""

    __primary_key__ = ("id",)
    __auto_increment__ = ("id",)
    __unique__ = ()
    __unique_sets__ = (("action_group_id", "name"),)
    __foreign_keys__ = {
        "action_group_id": ForeignKey(target="ActionGroup", field="id", cardinality="many_to_one"),
        "asset_id": ForeignKey(target="Asset", field="id", cardinality="many_to_one"),
        "account_id": ForeignKey(target="Account", field="id", cardinality="many_to_one"),
        "partial_group_id": ForeignKey(
            target="PartialGroup", field="id", cardinality="many_to_one"
        ),
        "trailing_group_id": ForeignKey(
            target="TrailingGroup", field="id", cardinality="many_to_one"
        ),
    }
    __credentials__ = {}

    id: int = Field(...)
    name: str = Field(...)
    action_group_id: int = Field(...)
    asset_id: int = Field(...)
    account_id: int = Field(...)
    partial_group_id: int = Field(...)
    trailing_group_id: int = Field(...)
    risk_by_reward: Decimal = Field(...)
    take_profit: Decimal = Field(...)
    stop_loss: Decimal = Field(...)
    is_active: bool = Field(default=True)
    description: str | None = Field(default=None)
