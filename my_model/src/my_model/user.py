"""The User domain entity: an independent user of the system."""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import Field

from my_model._base import BaseModel
from my_model._initial_data import GENERATE_SECURELY


class User(BaseModel):
    """An independent user of the system, enabling multi-user operation.

    Each user can have a separate set of settings, allowing new users to be
    added with configurations that remain distinct from those of existing
    users.
    """

    UNIQUE_TOGETHER: ClassVar[tuple[tuple[str, ...], ...]] = (("name",),)
    INITIAL_DATA: ClassVar[tuple[dict[str, Any], ...]] = (
        {
            "name": "Admin",
            "username": "admin",
            "password": GENERATE_SECURELY,
            "api_key": GENERATE_SECURELY,
        },
    )

    id: int | None = Field(
        default=None,
        description="Assigned by generation before the record is considered complete.",
    )
    name: str = Field(description="The user's display name.")
    username: str = Field(description="The username used to identify the user.")
    password: str = Field(
        repr=False,
        json_schema_extra={"credential": True, "storage_at_rest": "hash"},
        description="The password credential used by the user.",
    )
    api_key: str = Field(
        repr=False,
        json_schema_extra={"credential": True, "storage_at_rest": "hash"},
        description="The API key assigned to the user.",
    )
    status: bool = Field(
        default=True, description="Indicates whether the user is active."
    )
    description: str | None = Field(default=None, description="Describes the user.")
