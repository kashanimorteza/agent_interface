"""The User Domain Definition (Target: Model > User)."""

from __future__ import annotations

from typing import ClassVar

import pydantic

from model.foundation import (
    ModelFoundation,
    description_field,
    id_field,
    is_active_field,
)


class User(ModelFoundation):
    """An independent user of the system, enabling multi-user operation with settings that
    remain distinct from those of other users."""

    CREDENTIAL_STORAGE: ClassVar[dict[str, str]] = {
        "password": "hash",
        "api_key": "hash",
    }

    id: int = id_field()
    name: str = pydantic.Field(description="The user's display name.")
    username: str = pydantic.Field(
        description="The username used to identify the user."
    )
    password: str = pydantic.Field(
        description="The password credential used by the user."
    )
    api_key: str = pydantic.Field(description="The API key assigned to the user.")
    is_active: bool = is_active_field("Indicates whether the user is active.")
    description: str | None = description_field("Describes the user.")
