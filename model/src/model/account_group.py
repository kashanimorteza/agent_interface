"""The Account Group Domain Definition."""

from __future__ import annotations

from pydantic import Field

from .foundation import ModelBase


class AccountGroup(ModelBase):
    """An independent group for organizing trading accounts owned by one user."""

    UNIQUE_CONSTRAINTS = (("user_id", "name"),)

    id: int | None = Field(default=None, description="Auto-incrementing primary key.")
    user_id: int = Field(..., description="Identifies the user who owns the account group.")
    name: str = Field(..., description="The account group's display name.")
    is_active: bool = Field(default=True, description="Whether the account group is active.")
    description: str | None = Field(default=None, description="Describes the account group.")
