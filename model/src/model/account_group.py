"""The Account Group Domain Definition."""

from __future__ import annotations

from typing import ClassVar

from model.foundation import ModelBase, persistence_field


class AccountGroup(ModelBase):
    """An independent group for organizing trading accounts owned by one user."""

    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (("user_id", "name"),)

    id: int = persistence_field(
        primary_key=True,
        auto_increment=True,
        description="Primary identity of the account group.",
    )
    user_id: int = persistence_field(
        foreign_key="user.id",
        description="Identifies the user who owns the account group.",
    )
    name: str = persistence_field(description="The account group's display name.")
    is_active: bool = persistence_field(
        default=True, description="Indicates whether the account group is active."
    )
    description: str | None = persistence_field(
        default=None, description="Describes the account group."
    )
