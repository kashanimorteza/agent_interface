"""An independent user of the system."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from ._base import DomainModel, credential_field
from ._generation import GENERATE_SECURELY


class User(DomainModel):
    """An independent user, enabling multi-user operation with separate settings."""

    id: int | None = Field(default=None, description="Primary key, auto-incremented.")
    name: str = Field(description="The user's display name.", json_schema_extra={"unique": True})
    username: str = Field(description="The username used to identify the user.")
    password: str = credential_field(description="The password credential used by the user.")
    api_key: str = credential_field(description="The API key assigned to the user.")
    status: bool = Field(default=True, description="Indicates whether the user is active.")
    description: str | None = Field(default=None, description="Describes the user.")


INITIAL_DATA: tuple[dict[str, Any], ...] = (
    {
        "name": "Admin",
        "username": "admin",
        "password": GENERATE_SECURELY,
        "api_key": GENERATE_SECURELY,
    },
)
