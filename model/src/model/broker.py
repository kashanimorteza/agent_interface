"""The Broker Domain Definition."""

from __future__ import annotations

from typing import ClassVar

from model.foundation import ModelBase, persistence_field


class Broker(ModelBase):
    """A broker supported by the system, owned by the user who configured it.

    Not coupled to one Trading Platform.
    """

    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (("user_id", "name"),)

    id: int = persistence_field(
        primary_key=True,
        auto_increment=True,
        description="Primary identity of the broker.",
    )
    name: str = persistence_field(description="The broker's display name.")
    user_id: int = persistence_field(
        foreign_key="user.id",
        description="Identifies the user who owns the broker configuration.",
    )
    is_active: bool = persistence_field(
        default=True, description="Indicates whether the broker is active."
    )
    description: str | None = persistence_field(
        default=None, description="Describes the broker."
    )
