"""An independent group of rules for managing portions of an open trade."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from ._base import DomainModel


class PartialGroup(DomainModel):
    """A group that identifies a set of Partial Rules owned by one User."""

    unique_together = (("user_id", "name"),)

    id: int | None = Field(default=None, description="Primary key, auto-incremented.")
    user_id: int = Field(description="Identifies the user who owns the partial group.")
    name: str = Field(description="The partial group's display name.")
    status: bool = Field(default=True, description="Indicates whether the partial group is active.")
    description: str | None = Field(default=None, description="Describes the partial group.")


INITIAL_DATA: tuple[dict[str, Any], ...] = ({"user_id": 1, "name": "Default"},)
