"""The Broker Domain Definition."""

from __future__ import annotations

from pydantic import Field

from .foundation import ModelBase


class Broker(ModelBase):
    """A broker supported by the system, owned by a user, independent of any Trading Platform."""

    UNIQUE_CONSTRAINTS = (("user_id", "name"),)

    id: int | None = Field(default=None, description="Auto-incrementing primary key.")
    name: str = Field(..., description="The broker's display name.")
    user_id: int = Field(..., description="Identifies the user who owns the broker configuration.")
    is_active: bool = Field(default=True, description="Whether the broker is active.")
    description: str | None = Field(default=None, description="Describes the broker.")
