"""The Trailing Group Domain Definition."""

from __future__ import annotations

from pydantic import Field

from .foundation import ModelBase


class TrailingGroup(ModelBase):
    """An independent group for organizing the rules that manage Stop Loss and Take Profit."""

    UNIQUE_CONSTRAINTS = (("user_id", "name"),)

    id: int | None = Field(default=None, description="Auto-incrementing primary key.")
    user_id: int = Field(..., description="Identifies the user who owns the trailing group.")
    name: str = Field(..., description="The trailing group's display name.")
    is_active: bool = Field(default=True, description="Whether the trailing group is active.")
    description: str | None = Field(default=None, description="Describes the trailing group.")
