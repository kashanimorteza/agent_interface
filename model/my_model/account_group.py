"""Account Group: an independent group for organizing trading accounts."""

from __future__ import annotations

from .base import Model, field


class AccountGroup(Model):
    """Defines an independent group for organizing trading accounts."""

    logical_name = "Account Group"

    id: int | None = field("integer", primary_key=True, auto_increment=True)
    name: str = field("string", unique=True, purpose="The account group's display name.")
    status: bool = field("boolean", default=True, purpose="Indicates whether the account group is active.")
    description: str | None = field("string", nullable=True, purpose="Describes the account group.")

    initial_data = ({"name": "Default"},)
