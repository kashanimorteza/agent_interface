"""The Action Domain Definition (Target: Model > Action)."""

from __future__ import annotations

import pydantic

from model.foundation import (
    ExactDecimal,
    ModelFoundation,
    description_field,
    id_field,
    is_active_field,
)


class Action(ModelFoundation):
    """Defines how a position must be opened. An action selects the asset and account and
    provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that
    determine the position's parameters and execution behavior."""

    id: int = id_field()
    name: str = pydantic.Field(description="The action's display name.")
    action_group_id: int = pydantic.Field(
        description="Identifies the action group that contains the action."
    )
    asset_id: int = pydantic.Field(
        description="Identifies the asset traded by the action."
    )
    account_id: int = pydantic.Field(
        description="Identifies the account used to execute the action."
    )
    partial_group_id: int = pydantic.Field(
        description="Identifies the Partial Group used by the action."
    )
    trailing_group_id: int = pydantic.Field(
        description="Identifies the Trailing Group used by the action."
    )
    risk_by_reward: ExactDecimal = pydantic.Field(
        description="Defines the numeric risk-to-reward value used by the action."
    )
    take_profit: ExactDecimal = pydantic.Field(
        description="Defines the Take Profit value used by the action."
    )
    stop_loss: ExactDecimal = pydantic.Field(
        description="Defines the Stop Loss value used by the action."
    )
    is_active: bool = is_active_field("Indicates whether the action is active.")
    description: str | None = description_field("Describes the action.")
