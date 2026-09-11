"""An independent group for organizing trading accounts owned by one user."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from ._base import DomainModel


class AccountGroup(DomainModel):
    """A group that organizes a User's trading accounts."""

    unique_together = (("user_id", "name"),)

    id: int | None = Field(default=None, description="Primary key, auto-incremented.")
    user_id: int = Field(description="Identifies the user who owns the account group.")
    name: str = Field(description="The account group's display name.")
    status: bool = Field(default=True, description="Indicates whether the account group is active.")
    description: str | None = Field(default=None, description="Describes the account group.")


INITIAL_DATA: tuple[dict[str, Any], ...] = ({"user_id": 1, "name": "Default"},)
