"""The Partial Group domain entity."""

from __future__ import annotations

from pydantic import Field

from ._base import BaseModel


class PartialGroup(BaseModel):
    """An independent group of rules for managing how much of an open trade must
    be closed when profit or loss reaches specified thresholds.
    """

    initial_data = ({"user_id": 1, "name": "Default"},)

    id: int | None = Field(
        default=None, description="System-generated identity, absent until persisted."
    )
    user_id: int = Field(description="Identifies the user who owns the partial group.")
    name: str = Field(min_length=1, description="The partial group's display name.")
    status: bool = Field(default=True, description="Whether the partial group is active.")
    description: str | None = Field(default=None, description="Describes the partial group.")
