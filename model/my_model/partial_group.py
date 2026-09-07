"""Partial Group: a group of rules for managing portions of an open trade."""

from __future__ import annotations

from .base import Model, field


class PartialGroup(Model):
    """Defines an independent group of rules for managing portions of an open
    trade. Its rules determine how much of the trade volume must be closed
    when profit or loss reaches specified thresholds."""

    logical_name = "Partial Group"

    id: int | None = field("integer", primary_key=True, auto_increment=True)
    name: str = field("string", unique=True, purpose="The partial group's display name.")
    status: bool = field("boolean", default=True, purpose="Indicates whether the partial group is active.")
    description: str | None = field("string", nullable=True, purpose="Describes the partial group.")

    initial_data = ({"name": "Default"},)
