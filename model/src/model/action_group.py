"""The Action Group Domain Definition (Target: Model > Action Group)."""

from __future__ import annotations

import pydantic

from model.foundation import (
    ModelFoundation,
    description_field,
    id_field,
    is_active_field,
)


class ActionGroup(ModelFoundation):
    """An independent grouping for trading actions based on their risk profile, such as high
    risk, normal risk, or low risk. Actions are assigned to these groups so trades can be
    organized and selected by their intended risk level."""

    id: int = id_field()
    user_id: int = pydantic.Field(
        description="Identifies the user who owns the action group."
    )
    name: str = pydantic.Field(description="The action group's display name.")
    is_active: bool = is_active_field("Indicates whether the action group is active.")
    description: str | None = description_field("Describes the action group.")
