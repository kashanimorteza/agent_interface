"""The Partial Group Domain Definition."""

from __future__ import annotations

from pydantic import Field

from .foundation import ModelBase


class PartialGroup(ModelBase):
    """An independent group of rules for managing portions of an open trade."""

    UNIQUE_CONSTRAINTS = (("user_id", "name"),)

    id: int | None = Field(default=None, description="Auto-incrementing primary key.")
    user_id: int = Field(..., description="Identifies the user who owns the partial group.")
    name: str = Field(..., description="The partial group's display name.")
    is_active: bool = Field(default=True, description="Whether the partial group is active.")
    description: str | None = Field(default=None, description="Describes the partial group.")
