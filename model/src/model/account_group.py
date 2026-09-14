"""The Account Group Domain Definition (Target: Model > Account Group)."""

from __future__ import annotations

import pydantic

from model.foundation import (
    ModelFoundation,
    description_field,
    id_field,
    is_active_field,
)


class AccountGroup(ModelFoundation):
    """An independent group for organizing trading accounts owned by one user."""

    id: int = id_field()
    user_id: int = pydantic.Field(
        description="Identifies the user who owns the account group."
    )
    name: str = pydantic.Field(description="The account group's display name.")
    is_active: bool = is_active_field("Indicates whether the account group is active.")
    description: str | None = description_field("Describes the account group.")
