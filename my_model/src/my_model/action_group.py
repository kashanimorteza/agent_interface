"""The Action Group domain entity."""

from __future__ import annotations

from pydantic import Field

from ._base import BaseModel


class ActionGroup(BaseModel):
    """An independent grouping for trading actions based on their risk profile,
    such as high, normal, or low risk.
    """

    initial_data = ({"user_id": 1, "name": "Default"},)

    id: int | None = Field(
        default=None, description="System-generated identity, absent until persisted."
    )
    user_id: int = Field(description="Identifies the user who owns the action group.")
    name: str = Field(min_length=1, description="The action group's display name.")
    status: bool = Field(default=True, description="Whether the action group is active.")
    description: str | None = Field(default=None, description="Describes the action group.")
