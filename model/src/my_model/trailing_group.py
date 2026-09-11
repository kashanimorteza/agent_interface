"""An independent group for organizing rules that manage Stop Loss and Take Profit during a trade."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from ._base import DomainModel


class TrailingGroup(DomainModel):
    """A group that identifies a set of Trailing Rules owned by one User."""

    unique_together = (("user_id", "name"),)

    id: int | None = Field(default=None, description="Primary key, auto-incremented.")
    user_id: int = Field(description="Identifies the user who owns the trailing group.")
    name: str = Field(description="The trailing group's display name.")
    status: bool = Field(default=True, description="Indicates whether the trailing group is active.")
    description: str | None = Field(default=None, description="Describes the trailing group.")


INITIAL_DATA: tuple[dict[str, Any], ...] = ({"user_id": 1, "name": "Default"},)
