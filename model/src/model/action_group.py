"""The Action Group Domain Definition."""

from __future__ import annotations

from typing import ClassVar

from model.foundation import ModelBase, persistence_field


class ActionGroup(ModelBase):
    """An independent grouping for trading actions based on their risk profile.

    Such as high risk, normal risk, or low risk. Actions are assigned to
    these groups so trades can be organized and selected by their intended
    risk level.
    """

    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (("user_id", "name"),)

    id: int = persistence_field(
        primary_key=True,
        auto_increment=True,
        description="Primary identity of the action group.",
    )
    user_id: int = persistence_field(
        foreign_key="user.id",
        description="Identifies the user who owns the action group.",
    )
    name: str = persistence_field(description="The action group's display name.")
    is_active: bool = persistence_field(
        default=True, description="Indicates whether the action group is active."
    )
    description: str | None = persistence_field(
        default=None, description="Describes the action group."
    )
