"""The Partial Group domain entity: a group of partial-close rules."""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import Field

from my_model._base import BaseModel


class PartialGroup(BaseModel):
    """An independent group of rules for managing portions of an open trade.

    Its rules determine how much of the trade volume must be closed when
    profit or loss reaches specified thresholds.
    """

    UNIQUE_TOGETHER: ClassVar[tuple[tuple[str, ...], ...]] = (("user_id", "name"),)
    INITIAL_DATA: ClassVar[tuple[dict[str, Any], ...]] = (
        {"user_id": 1, "name": "Default"},
    )

    id: int | None = Field(
        default=None,
        description="Assigned by generation before the record is considered complete.",
    )
    user_id: int = Field(description="Identifies the user who owns the partial group.")
    name: str = Field(description="The partial group's display name.")
    status: bool = Field(
        default=True, description="Indicates whether the partial group is active."
    )
    description: str | None = Field(
        default=None, description="Describes the partial group."
    )
