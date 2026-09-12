"""The Broker domain entity."""

from __future__ import annotations

from pydantic import Field

from ._base import BaseModel


class Broker(BaseModel):
    """A broker supported by the system, owned by a user, kept independent of any
    one Trading Platform.
    """

    initial_data = ({"name": "FxPro", "user_id": 1},)

    id: int | None = Field(
        default=None, description="System-generated identity, absent until persisted."
    )
    name: str = Field(min_length=1, description="The broker's display name.")
    user_id: int = Field(description="Identifies the user who owns the broker configuration.")
    status: bool = Field(default=True, description="Whether the broker is active.")
    description: str | None = Field(default=None, description="Describes the broker.")
