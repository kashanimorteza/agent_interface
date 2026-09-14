"""The Trailing Rule Domain Definition (Target: Model > Trailing Rule)."""

from __future__ import annotations

import pydantic

from model.foundation import (
    ExactDecimal,
    ModelFoundation,
    description_field,
    id_field,
    is_active_field,
)


class TrailingRule(ModelFoundation):
    """An individual rule within a Trailing Group that tells the system when and how to manage
    Take Profit and Stop Loss, providing the activation condition and the parameters used to
    apply the required adjustments."""

    id: int = id_field()
    name: str = pydantic.Field(description="The trailing rule's display name.")
    trailing_group_id: int = pydantic.Field(
        description="Identifies the trailing group that contains the rule."
    )
    trigger_percentage: ExactDecimal = pydantic.Field(
        description="Defines the profit percentage of the take-profit target that activates the rule."
    )
    take_profit_adjustment: ExactDecimal | None = pydantic.Field(
        default=None,
        description="Defines the take-profit adjustment applied when the rule is activated.",
    )
    stop_loss_adjustment: ExactDecimal | None = pydantic.Field(
        default=None,
        description="Defines the stop-loss adjustment applied when the rule is activated.",
    )
    is_active: bool = is_active_field("Indicates whether the trailing rule is active.")
    description: str | None = description_field("Describes the trailing rule.")
