"""The Account Group domain entity: a group organizing trading accounts."""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import Field

from my_model._base import BaseModel


class AccountGroup(BaseModel):
    """An independent group for organizing trading accounts owned by one user."""

    UNIQUE_TOGETHER: ClassVar[tuple[tuple[str, ...], ...]] = (("user_id", "name"),)
    INITIAL_DATA: ClassVar[tuple[dict[str, Any], ...]] = (
        {"user_id": 1, "name": "Default"},
    )

    id: int | None = Field(
        default=None,
        description="Assigned by generation before the record is considered complete.",
    )
    user_id: int = Field(description="Identifies the user who owns the account group.")
    name: str = Field(description="The account group's display name.")
    status: bool = Field(
        default=True, description="Indicates whether the account group is active."
    )
    description: str | None = Field(
        default=None, description="Describes the account group."
    )
