"""The Account Group domain entity."""

from __future__ import annotations

from pydantic import Field

from ._base import BaseModel


class AccountGroup(BaseModel):
    """An independent group for organizing trading accounts owned by one user."""

    initial_data = ({"user_id": 1, "name": "Default"},)

    id: int | None = Field(
        default=None, description="System-generated identity, absent until persisted."
    )
    user_id: int = Field(description="Identifies the user who owns the account group.")
    name: str = Field(min_length=1, description="The account group's display name.")
    status: bool = Field(default=True, description="Whether the account group is active.")
    description: str | None = Field(default=None, description="Describes the account group.")
