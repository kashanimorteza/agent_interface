"""The Action Group Domain Definition."""

from __future__ import annotations

from pydantic import Field

from .foundation import ModelBase


class ActionGroup(ModelBase):
    """An independent grouping for trading actions based on their risk profile."""

    UNIQUE_CONSTRAINTS = (("user_id", "name"),)

    id: int | None = Field(default=None, description="Auto-incrementing primary key.")
    user_id: int = Field(..., description="Identifies the user who owns the action group.")
    name: str = Field(..., description="The action group's display name.")
    is_active: bool = Field(default=True, description="Whether the action group is active.")
    description: str | None = Field(default=None, description="Describes the action group.")
