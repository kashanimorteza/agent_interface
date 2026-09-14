"""The Partial Rule Domain Definition (Target: Model > Partial Rule)."""

from __future__ import annotations

import pydantic

from model.foundation import (
    ExactDecimal,
    ModelFoundation,
    description_field,
    id_field,
    is_active_field,
)


class PartialRule(ModelFoundation):
    """An individual Partial Close rule that tells the system under which condition part of an
    open position must be closed and how much of its volume must be closed."""

    id: int = id_field()
    name: str = pydantic.Field(description="The partial rule's display name.")
    partial_group_id: int = pydantic.Field(
        description="Identifies the partial group that contains the rule."
    )
    profit_percentage: ExactDecimal = pydantic.Field(
        description="Defines the profit percentage that activates the rule."
    )
    close_percentage: ExactDecimal = pydantic.Field(
        description="Defines the percentage of the position closed when the rule is activated."
    )
    is_active: bool = is_active_field("Indicates whether the partial rule is active.")
    description: str | None = description_field("Describes the partial rule.")
