"""The Partial Rule Domain Definition."""

from __future__ import annotations

from decimal import Decimal
from typing import ClassVar

from model.foundation import ModelBase, persistence_field


class PartialRule(ModelBase):
    """One Partial Close rule.

    Tells the system under which condition part of an open position must be
    closed and how much of its volume must be closed.
    """

    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (
        ("partial_group_id", "profit_percentage"),
    )

    id: int = persistence_field(
        primary_key=True,
        auto_increment=True,
        description="Primary identity of the partial rule.",
    )
    name: str = persistence_field(
        unique=True, description="The partial rule's display name."
    )
    partial_group_id: int = persistence_field(
        foreign_key="partial_group.id",
        description="Identifies the partial group that contains the rule.",
    )
    profit_percentage: Decimal = persistence_field(
        description="Defines the profit percentage that activates the rule."
    )
    close_percentage: Decimal = persistence_field(
        description="Defines the percentage of the position closed when the rule is activated."
    )
    is_active: bool = persistence_field(
        default=True, description="Indicates whether the partial rule is active."
    )
    description: str | None = persistence_field(
        default=None, description="Describes the partial rule."
    )
