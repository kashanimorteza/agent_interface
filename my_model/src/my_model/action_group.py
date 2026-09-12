"""The Action Group domain entity: a risk-profile grouping for Actions."""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import Field

from my_model._base import BaseModel


class ActionGroup(BaseModel):
    """An independent grouping for trading actions based on their risk
    profile, such as high risk, normal risk, or low risk.

    Actions are assigned to these groups so trades can be organized and
    selected by their intended risk level.
    """

    UNIQUE_TOGETHER: ClassVar[tuple[tuple[str, ...], ...]] = (("user_id", "name"),)
    INITIAL_DATA: ClassVar[tuple[dict[str, Any], ...]] = (
        {"user_id": 1, "name": "Default"},
    )

    id: int | None = Field(
        default=None,
        description="Assigned by generation before the record is considered complete.",
    )
    user_id: int = Field(description="Identifies the user who owns the action group.")
    name: str = Field(description="The action group's display name.")
    status: bool = Field(
        default=True, description="Indicates whether the action group is active."
    )
    description: str | None = Field(
        default=None, description="Describes the action group."
    )
