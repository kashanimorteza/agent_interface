"""The Trailing Group Domain Definition."""

from __future__ import annotations

from typing import ClassVar

from model.foundation import ModelBase, persistence_field


class TrailingGroup(ModelBase):
    """An independent group for organizing the rules that manage Stop Loss and Take Profit during a trade.

    The group identifies the rule set, while each Trailing Rule separately
    defines its activation condition and the changes to apply.
    """

    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (("user_id", "name"),)

    id: int = persistence_field(
        primary_key=True,
        auto_increment=True,
        description="Primary identity of the trailing group.",
    )
    user_id: int = persistence_field(
        foreign_key="user.id",
        description="Identifies the user who owns the trailing group.",
    )
    name: str = persistence_field(description="The trailing group's display name.")
    is_active: bool = persistence_field(
        default=True, description="Indicates whether the trailing group is active."
    )
    description: str | None = persistence_field(
        default=None, description="Describes the trailing group."
    )
