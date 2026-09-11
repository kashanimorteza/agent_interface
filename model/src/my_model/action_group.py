"""An independent grouping for trading actions based on their risk profile."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from ._base import DomainModel


class ActionGroup(DomainModel):
    """A risk-profile group that organizes a User's trading Actions."""

    unique_together = (("user_id", "name"),)

    id: int | None = Field(default=None, description="Primary key, auto-incremented.")
    user_id: int = Field(description="Identifies the user who owns the action group.")
    name: str = Field(description="The action group's display name.")
    status: bool = Field(default=True, description="Indicates whether the action group is active.")
    description: str | None = Field(default=None, description="Describes the action group.")


INITIAL_DATA: tuple[dict[str, Any], ...] = ({"user_id": 1, "name": "Default"},)
