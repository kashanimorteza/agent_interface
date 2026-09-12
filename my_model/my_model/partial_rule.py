"""The Partial Rule domain entity."""

from decimal import Decimal

from pydantic import Field

from my_model._base import BaseModel


class PartialRule(BaseModel):
    """An individual Partial Close rule telling the system under which
    condition part of an open position must be closed and how much of its
    volume must be closed.
    """

    id: int = Field(description="The partial rule's logical identity.")
    name: str = Field(description="The partial rule's display name.")
    partial_group_id: int = Field(description="Identifies the partial group that contains the rule.")
    profit_percentage: Decimal = Field(description="The profit percentage that activates the rule.")
    close_percentage: Decimal = Field(
        description="The percentage of the position closed when the rule is activated."
    )
    status: bool = Field(default=True, description="Whether the partial rule is active.")
    description: str | None = Field(default=None, description="Describes the partial rule.")
