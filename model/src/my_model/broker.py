"""A broker supported by the system, independent of any one Trading Platform."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from ._base import DomainModel


class Broker(DomainModel):
    """A broker owned by one User's configuration."""

    unique_together = (("user_id", "name"),)

    id: int | None = Field(default=None, description="Primary key, auto-incremented.")
    name: str = Field(description="The broker's display name.")
    user_id: int = Field(description="Identifies the user who owns the broker configuration.")
    status: bool = Field(default=True, description="Indicates whether the broker is active.")
    description: str | None = Field(default=None, description="Describes the broker.")


INITIAL_DATA: tuple[dict[str, Any], ...] = ({"name": "FxPro", "user_id": 1},)
