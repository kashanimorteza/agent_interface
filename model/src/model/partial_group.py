"""The Partial Group Domain Definition."""

from __future__ import annotations

from typing import ClassVar

from model.foundation import ModelBase, persistence_field


class PartialGroup(ModelBase):
    """An independent group of rules for managing portions of an open trade.

    Its rules determine how much of the trade volume must be closed when
    profit or loss reaches specified thresholds.
    """

    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (("user_id", "name"),)

    id: int = persistence_field(
        primary_key=True,
        auto_increment=True,
        description="Primary identity of the partial group.",
    )
    user_id: int = persistence_field(
        foreign_key="user.id",
        description="Identifies the user who owns the partial group.",
    )
    name: str = persistence_field(description="The partial group's display name.")
    is_active: bool = persistence_field(
        default=True, description="Indicates whether the partial group is active."
    )
    description: str | None = persistence_field(
        default=None, description="Describes the partial group."
    )
