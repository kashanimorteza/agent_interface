"""The Trailing Group domain entity: a group of Stop Loss/Take Profit rules."""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import Field

from my_model._base import BaseModel


class TrailingGroup(BaseModel):
    """An independent group for organizing the rules that manage Stop Loss
    and Take Profit during a trade.

    The group identifies the rule set, while each Trailing Rule separately
    defines its activation condition and the changes to apply.
    """

    UNIQUE_TOGETHER: ClassVar[tuple[tuple[str, ...], ...]] = (("user_id", "name"),)
    INITIAL_DATA: ClassVar[tuple[dict[str, Any], ...]] = (
        {"user_id": 1, "name": "Default"},
    )

    id: int | None = Field(
        default=None,
        description="Assigned by generation before the record is considered complete.",
    )
    user_id: int = Field(description="Identifies the user who owns the trailing group.")
    name: str = Field(description="The trailing group's display name.")
    status: bool = Field(
        default=True, description="Indicates whether the trailing group is active."
    )
    description: str | None = Field(
        default=None, description="Describes the trailing group."
    )
