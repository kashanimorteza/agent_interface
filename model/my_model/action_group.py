"""Action Group: a grouping of trading actions by risk profile."""

from __future__ import annotations

from .base import Model, field


class ActionGroup(Model):
    """Defines an independent grouping for trading actions based on their
    risk profile, such as high risk, normal risk, or low risk. Actions are
    assigned to these groups so trades can be organized and selected by their
    intended risk level."""

    logical_name = "Action Group"

    id: int | None = field("integer", primary_key=True, auto_increment=True)
    name: str = field("string", unique=True, purpose="The action group's display name.")
    status: bool = field("boolean", default=True, purpose="Indicates whether the action group is active.")
    description: str | None = field("string", nullable=True, purpose="Describes the action group.")

    initial_data = ({"name": "Default"},)
