"""The PartialRule Model."""

from decimal import Decimal
from pydantic import Field

from ._base import Model


class PartialRule(Model):
    """Defines an individual Partial Close rule that tells the system under which condition part of an
    open position must be closed and how much of its volume must be closed.
    """

    id: int | None = Field(default=None, description="Assigned by persistence on create; absent until then.")
    name: str = Field(description="The partial rule's display name. Unique.")
    partial_group_id: int = Field(description="Identifies the partial group that contains the rule.")
    profit_percentage: Decimal = Field(description="Defines the profit percentage that activates the rule.")
    close_percentage: Decimal = Field(
        description="Defines the percentage of the position closed when the rule is activated.",
    )
    status: bool = Field(default=True, description="Indicates whether the partial rule is active.")
    description: str | None = Field(default=None, description="Describes the partial rule.")
