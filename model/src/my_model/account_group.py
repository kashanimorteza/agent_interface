from __future__ import annotations

from typing import ClassVar

from pydantic import Field

from ._base import DomainModel
from ._shared import Relationship


class AccountGroup(DomainModel):
    user_id: int = Field(..., description="Identifies the user who owns the account group.")
    name: str = Field(..., description="The account group's display name.")
    status: bool = Field(default=True, description="Indicates whether the account group is active.")
    description: str | None = Field(default=None, description="Describes the account group.")

    unique_together: ClassVar[list[tuple[str, ...]]] = [("user_id", "name")]
    relationships: ClassVar[dict[str, Relationship]] = {
        "user": Relationship(target="User", cardinality="one", field="user_id"),
    }


ACCOUNT_GROUP_INITIAL_DATA: list[dict] = [
    {"user_id": 1, "name": "Default"},
]
