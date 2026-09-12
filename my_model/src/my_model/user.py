"""The User domain entity."""

from __future__ import annotations

from pydantic import Field

from ._base import GENERATE_SECURELY, BaseModel


class User(BaseModel):
    """An independent user of the system, enabling multi-user operation with each
    user's settings kept distinct from every other user's.
    """

    credential_fields = frozenset({"password", "api_key"})
    initial_data = (
        {
            "name": "Admin",
            "username": "admin",
            "password": GENERATE_SECURELY,
            "api_key": GENERATE_SECURELY,
        },
    )

    id: int | None = Field(
        default=None, description="System-generated identity, absent until persisted."
    )
    name: str = Field(min_length=1, description="The user's unique display name.")
    username: str = Field(min_length=1, description="The username used to identify the user.")
    password: str = Field(min_length=1, description="The password credential used by the user.")
    api_key: str = Field(min_length=1, description="The API key assigned to the user.")
    status: bool = Field(default=True, description="Whether the user is active.")
    description: str | None = Field(default=None, description="Describes the user.")
