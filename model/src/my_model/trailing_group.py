from __future__ import annotations

from typing import ClassVar

from pydantic import Field

from ._base import DomainModel
from ._shared import Relationship


class TrailingGroup(DomainModel):
    user_id: int = Field(..., description="Identifies the user who owns the trailing group.")
    name: str = Field(..., description="The trailing group's display name.")
    status: bool = Field(default=True, description="Indicates whether the trailing group is active.")
    description: str | None = Field(default=None, description="Describes the trailing group.")

    unique_together: ClassVar[list[tuple[str, ...]]] = [("user_id", "name")]
    relationships: ClassVar[dict[str, Relationship]] = {
        "user": Relationship(target="User", cardinality="one", field="user_id"),
    }


TRAILING_GROUP_INITIAL_DATA: list[dict] = [
    {"user_id": 1, "name": "Default"},
]
