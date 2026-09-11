from decimal import Decimal

from pydantic import Field

from ._base import BaseModel


class PartialRule(BaseModel):
    """An individual Partial Close rule telling the system when and how much of an open position to close."""

    id: int | None = Field(
        default=None, description="Generated once the Partial Rule is persisted."
    )
    name: str = Field(description="The partial rule's display name.")
    partial_group_id: int = Field(
        description="Identifies the partial group that contains the rule."
    )
    profit_percentage: Decimal = Field(
        description="The profit percentage that activates the rule."
    )
    close_percentage: Decimal = Field(
        description="The percentage of the position closed when the rule is activated."
    )
    status: bool = Field(
        default=True, description="Indicates whether the partial rule is active."
    )
    description: str | None = Field(
        default=None, description="Describes the partial rule."
    )
