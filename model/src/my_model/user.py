from __future__ import annotations

from typing import ClassVar

from pydantic import Field

from ._base import DomainModel


class User(DomainModel):
    name: str = Field(..., description="The user's display name.")
    username: str = Field(..., description="The username used to identify the user.")
    password: str = Field(..., description="The password credential used by the user.")
    api_key: str = Field(..., description="The API key assigned to the user.")
    status: bool = Field(default=True, description="Indicates whether the user is active.")
    description: str | None = Field(default=None, description="Describes the user.")

    unique_fields: ClassVar[frozenset[str]] = frozenset({"name"})
    credential_fields: ClassVar[frozenset[str]] = frozenset({"password", "api_key"})
    credential_storage: ClassVar[dict[str, str]] = {"password": "hash", "api_key": "hash"}


USER_INITIAL_DATA: list[dict] = [
    {
        "name": "Admin",
        "username": "admin",
        "password": "<generate securely>",
        "api_key": "<generate securely>",
    },
]
