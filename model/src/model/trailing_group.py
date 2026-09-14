"""The Trailing Group Domain Definition (Target: Model > Trailing Group)."""

from __future__ import annotations

import pydantic

from model.foundation import (
    ModelFoundation,
    description_field,
    id_field,
    is_active_field,
)


class TrailingGroup(ModelFoundation):
    """An independent group for organizing the rules that manage Stop Loss and Take Profit
    during a trade. The group identifies the rule set, while each rule separately defines its
    activation condition and the changes to apply."""

    id: int = id_field()
    user_id: int = pydantic.Field(
        description="Identifies the user who owns the trailing group."
    )
    name: str = pydantic.Field(description="The trailing group's display name.")
    is_active: bool = is_active_field("Indicates whether the trailing group is active.")
    description: str | None = description_field("Describes the trailing group.")
