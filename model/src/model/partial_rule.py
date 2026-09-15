"""Domain Definition for Partial Rule."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from model.foundation import DomainModel, ForeignKey


class PartialRule(DomainModel):
    """Defines an individual Partial Close rule that tells the system under which condition
    part of an open position must be closed and how much of its volume must be closed.
    """

    __primary_key__ = ("id",)
    __auto_increment__ = ("id",)
    __unique__ = ("name",)
    __unique_sets__ = (("partial_group_id", "profit_percentage"),)
    __foreign_keys__ = {
        "partial_group_id": ForeignKey(target="PartialGroup", field="id", cardinality="many_to_one")
    }
    __credentials__ = {}

    id: int = Field(...)
    name: str = Field(...)
    partial_group_id: int = Field(...)
    profit_percentage: Decimal = Field(...)
    close_percentage: Decimal = Field(...)
    is_active: bool = Field(default=True)
    description: str | None = Field(default=None)
