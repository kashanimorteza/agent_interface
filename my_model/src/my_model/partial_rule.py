"""The Partial Rule domain entity."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from ._base import BaseModel


class PartialRule(BaseModel):
    """An individual Partial Close rule telling the system under which profit
    condition part of an open position must be closed and how much of its volume
    must be closed.
    """

    id: int | None = Field(
        default=None, description="System-generated identity, absent until persisted."
    )
    name: str = Field(min_length=1, description="The partial rule's unique display name.")
    partial_group_id: int = Field(
        description="Identifies the partial group that contains the rule."
    )
    profit_percentage: Decimal = Field(
        ge=0, description="The profit percentage that activates the rule."
    )
    close_percentage: Decimal = Field(
        gt=0,
        le=100,
        description="The percentage of the position closed when the rule is activated.",
    )
    status: bool = Field(default=True, description="Whether the partial rule is active.")
    description: str | None = Field(default=None, description="Describes the partial rule.")
