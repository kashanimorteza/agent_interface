"""The Partial Group domain Model: an independent group organizing Partial Rules."""

from pydantic import Field

from ._base import BaseModel


class PartialGroup(BaseModel):
    """An independent group of rules for managing portions of an open trade.

    Its rules determine how much of the trade volume must be closed when
    profit or loss reaches specified thresholds. The combination-uniqueness of
    `user_id` and `name` is a domain rule traceable to this Model, enforced by
    Database.
    """

    id: int | None = Field(default=None, description="The partial group's generated identity.")
    user_id: int = Field(description="Identifies the user who owns the partial group.")
    name: str = Field(description="The partial group's display name.")
    status: bool = Field(
        default=True, description="Indicates whether the partial group is active."
    )
    description: str | None = Field(default=None, description="Describes the partial group.")


INITIAL_DATA: list[dict[str, object]] = [
    {"user_id": 1, "name": "Default"},
]
