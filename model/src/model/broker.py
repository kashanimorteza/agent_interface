"""The Broker Domain Definition (Target: Model > Broker)."""

from __future__ import annotations

import pydantic

from model.foundation import (
    ModelFoundation,
    description_field,
    id_field,
    is_active_field,
)


class Broker(ModelFoundation):
    """A broker supported by the system, owned by the user whose configuration it belongs to,
    without coupling the Broker definition to one Trading Platform."""

    id: int = id_field()
    name: str = pydantic.Field(description="The broker's display name.")
    user_id: int = pydantic.Field(
        description="Identifies the user who owns the broker configuration."
    )
    is_active: bool = is_active_field("Indicates whether the broker is active.")
    description: str | None = description_field("Describes the broker.")
