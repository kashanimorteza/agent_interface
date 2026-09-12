"""The Trailing Group domain entity."""

from pydantic import Field

from my_model._base import BaseModel


class TrailingGroup(BaseModel):
    """An independent group for organizing the rules that manage Stop Loss
    and Take Profit during a trade.

    The group identifies the rule set, while each Trailing Rule separately
    defines its activation condition and the changes to apply.
    """

    id: int = Field(description="The trailing group's logical identity.")
    user_id: int = Field(description="Identifies the user who owns the trailing group.")
    name: str = Field(description="The trailing group's display name.")
    status: bool = Field(default=True, description="Whether the trailing group is active.")
    description: str | None = Field(default=None, description="Describes the trailing group.")


INITIAL_DATA: list[dict[str, object]] = [
    {"user_id": 1, "name": "Default"},
]
