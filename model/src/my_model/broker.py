from __future__ import annotations

from typing import ClassVar

from pydantic import Field

from ._base import DomainModel
from ._shared import Relationship


class Broker(DomainModel):
    name: str = Field(..., description="The broker's display name.")
    user_id: int = Field(..., description="Identifies the user who owns the broker configuration.")
    status: bool = Field(default=True, description="Indicates whether the broker is active.")
    description: str | None = Field(default=None, description="Describes the broker.")

    unique_together: ClassVar[list[tuple[str, ...]]] = [("user_id", "name")]
    relationships: ClassVar[dict[str, Relationship]] = {
        "user": Relationship(target="User", cardinality="one", field="user_id"),
    }


BROKER_INITIAL_DATA: list[dict] = [
    {"name": "FxPro", "user_id": 1},
]
