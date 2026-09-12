"""The Partial Rule domain Model: one rule within a Partial Group."""

from pydantic import Field

from ._base import BaseModel
from .types import Percentage


class PartialRule(BaseModel):
    """An individual Partial Close rule.

    Tells the system under which condition part of an open position must be
    closed and how much of its volume must be closed. The
    combination-uniqueness of `partial_group_id` and `profit_percentage` is a
    domain rule traceable to this Model, enforced by Database.
    """

    id: int | None = Field(default=None, description="The partial rule's generated identity.")
    name: str = Field(description="The partial rule's display name.")
    partial_group_id: int = Field(
        description="Identifies the partial group that contains the rule."
    )
    profit_percentage: Percentage = Field(
        description="Defines the profit percentage that activates the rule."
    )
    close_percentage: Percentage = Field(
        description="Defines the percentage of the position closed when the rule is activated."
    )
    status: bool = Field(default=True, description="Indicates whether the partial rule is active.")
    description: str | None = Field(default=None, description="Describes the partial rule.")


INITIAL_DATA: list[dict[str, object]] = []
