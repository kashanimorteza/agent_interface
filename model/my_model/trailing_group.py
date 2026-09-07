"""Trailing Group: a group of rules managing Stop Loss and Take Profit."""

from __future__ import annotations

from .base import Model, field


class TrailingGroup(Model):
    """Defines an independent group for organizing the rules that manage Stop
    Loss and Take Profit during a trade. The group identifies the rule set,
    while each rule separately defines its activation condition and the
    changes to apply."""

    logical_name = "Trailing Group"

    id: int | None = field("integer", primary_key=True, auto_increment=True)
    name: str = field("string", unique=True, purpose="The trailing group's display name.")
    status: bool = field("boolean", default=True, purpose="Indicates whether the trailing group is active.")
    description: str | None = field("string", nullable=True, purpose="Describes the trailing group.")

    initial_data = ({"name": "Default"},)
