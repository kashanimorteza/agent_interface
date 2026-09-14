"""The User Domain Definition."""

from __future__ import annotations

from pydantic import Field

from .foundation import ModelBase


class User(ModelBase):
    """An independent user of the system, enabling multi-user operation."""

    UNIQUE_CONSTRAINTS = (("name",),)

    id: int | None = Field(default=None, description="Auto-incrementing primary key.")
    name: str = Field(..., description="The user's display name.")
    username: str = Field(..., description="The username used to identify the user.")
    password: str = Field(
        ...,
        json_schema_extra={"credential": True},
        description="The password credential used by the user.",
    )
    api_key: str = Field(
        ...,
        json_schema_extra={"credential": True},
        description="The API key assigned to the user.",
    )
    is_active: bool = Field(default=True, description="Whether the user is active.")
    description: str | None = Field(default=None, description="Describes the user.")
