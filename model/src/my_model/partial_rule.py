"""An individual Partial Close rule telling the system when and how much of a position to close."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from ._base import DomainModel


class PartialRule(DomainModel):
    """A rule that closes a percentage of an open position once a profit threshold is reached."""

    unique_together = (("partial_group_id", "profit_percentage"),)

    id: int | None = Field(default=None, description="Primary key, auto-incremented.")
    name: str = Field(description="The partial rule's display name.", json_schema_extra={"unique": True})
    partial_group_id: int = Field(description="Identifies the partial group that contains the rule.")
    profit_percentage: Decimal = Field(description="Defines the profit percentage that activates the rule.")
    close_percentage: Decimal = Field(
        description="Defines the percentage of the position closed when the rule is activated."
    )
    status: bool = Field(default=True, description="Indicates whether the partial rule is active.")
    description: str | None = Field(default=None, description="Describes the partial rule.")
