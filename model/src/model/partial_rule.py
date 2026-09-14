"""The Partial Rule Domain Definition."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from .foundation import ModelBase


class PartialRule(ModelBase):
    """An individual Partial Close rule that tells the system when to close part of a position."""

    UNIQUE_CONSTRAINTS = (
        ("name",),
        ("partial_group_id", "profit_percentage"),
    )

    id: int | None = Field(default=None, description="Auto-incrementing primary key.")
    name: str = Field(..., description="The partial rule's display name.")
    partial_group_id: int = Field(
        ..., description="Identifies the partial group that contains the rule."
    )
    profit_percentage: Decimal = Field(
        ..., description="Defines the profit percentage that activates the rule."
    )
    close_percentage: Decimal = Field(
        ..., description="Defines the percentage of the position closed when the rule is activated."
    )
    is_active: bool = Field(default=True, description="Whether the partial rule is active.")
    description: str | None = Field(default=None, description="Describes the partial rule.")
