"""The Partial Group Domain Definition (Target: Model > Partial Group)."""

from __future__ import annotations

import pydantic

from model.foundation import (
    ModelFoundation,
    description_field,
    id_field,
    is_active_field,
)


class PartialGroup(ModelFoundation):
    """An independent group of rules for managing portions of an open trade. Its rules
    determine how much of the trade volume must be closed when profit or loss reaches
    specified thresholds."""

    id: int = id_field()
    user_id: int = pydantic.Field(
        description="Identifies the user who owns the partial group."
    )
    name: str = pydantic.Field(description="The partial group's display name.")
    is_active: bool = is_active_field("Indicates whether the partial group is active.")
    description: str | None = description_field("Describes the partial group.")
