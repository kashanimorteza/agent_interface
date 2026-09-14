"""The Action Domain Definition."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from .foundation import ModelBase


class Action(ModelBase):
    """Defines how a position must be opened: the asset, account, risk, and management settings."""

    UNIQUE_CONSTRAINTS = (("action_group_id", "name"),)

    id: int | None = Field(default=None, description="Auto-incrementing primary key.")
    name: str = Field(..., description="The action's display name.")
    action_group_id: int = Field(
        ..., description="Identifies the action group that contains the action."
    )
    asset_id: int = Field(..., description="Identifies the asset traded by the action.")
    account_id: int = Field(..., description="Identifies the account used to execute the action.")
    partial_group_id: int = Field(
        ..., description="Identifies the Partial Group used by the action."
    )
    trailing_group_id: int = Field(
        ..., description="Identifies the Trailing Group used by the action."
    )
    risk_by_reward: Decimal = Field(
        ..., description="Defines the numeric risk-to-reward value used by the action."
    )
    take_profit: Decimal = Field(
        ..., description="Defines the Take Profit value used by the action."
    )
    stop_loss: Decimal = Field(..., description="Defines the Stop Loss value used by the action.")
    is_active: bool = Field(default=True, description="Whether the action is active.")
    description: str | None = Field(default=None, description="Describes the action.")
