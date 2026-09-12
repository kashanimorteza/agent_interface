"""The Trailing Group domain entity."""

from __future__ import annotations

from pydantic import Field

from ._base import BaseModel


class TrailingGroup(BaseModel):
    """An independent group for organizing the rules that manage Stop Loss and
    Take Profit adjustment during a trade.
    """

    initial_data = ({"user_id": 1, "name": "Default"},)

    id: int | None = Field(
        default=None, description="System-generated identity, absent until persisted."
    )
    user_id: int = Field(description="Identifies the user who owns the trailing group.")
    name: str = Field(min_length=1, description="The trailing group's display name.")
    status: bool = Field(default=True, description="Whether the trailing group is active.")
    description: str | None = Field(default=None, description="Describes the trailing group.")
