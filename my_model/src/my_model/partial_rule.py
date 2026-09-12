"""The Partial Rule domain entity: one activation rule within a Partial Group."""

from __future__ import annotations

from decimal import Decimal
from typing import ClassVar

from pydantic import Field

from my_model._base import BaseModel


class PartialRule(BaseModel):
    """An individual Partial Close rule that tells the system under which
    condition part of an open position must be closed and how much of its
    volume must be closed.
    """

    UNIQUE_TOGETHER: ClassVar[tuple[tuple[str, ...], ...]] = (
        ("name",),
        ("partial_group_id", "profit_percentage"),
    )

    id: int | None = Field(
        default=None,
        description="Assigned by generation before the record is considered complete.",
    )
    name: str = Field(description="The partial rule's display name.")
    partial_group_id: int = Field(
        description="Identifies the partial group that contains the rule."
    )
    profit_percentage: Decimal = Field(
        description="Defines the profit percentage that activates the rule."
    )
    close_percentage: Decimal = Field(
        description="Defines the percentage of the position closed when the rule is activated."
    )
    status: bool = Field(
        default=True, description="Indicates whether the partial rule is active."
    )
    description: str | None = Field(
        default=None, description="Describes the partial rule."
    )
