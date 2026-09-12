"""The Action domain entity."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from ._base import BaseModel


class Action(BaseModel):
    """How a position must be opened: the asset and account used, and the risk,
    Take Profit, Stop Loss, Partial Group, and Trailing Group settings that
    determine the resulting position's parameters and execution behavior.
    """

    initial_data = (
        {
            "name": "Default",
            "action_group_id": 1,
            "asset_id": 1,
            "account_id": 1,
            "partial_group_id": 1,
            "trailing_group_id": 1,
            "risk_by_reward": Decimal("1"),
            "take_profit": Decimal("1"),
            "stop_loss": Decimal("1"),
        },
    )

    id: int | None = Field(
        default=None, description="System-generated identity, absent until persisted."
    )
    name: str = Field(min_length=1, description="The action's display name.")
    action_group_id: int = Field(
        description="Identifies the action group that contains the action."
    )
    asset_id: int = Field(description="Identifies the asset traded by the action.")
    account_id: int = Field(description="Identifies the account used to execute the action.")
    partial_group_id: int = Field(description="Identifies the Partial Group used by the action.")
    trailing_group_id: int = Field(description="Identifies the Trailing Group used by the action.")
    risk_by_reward: Decimal = Field(
        description="The numeric risk-to-reward value used by the action."
    )
    take_profit: Decimal = Field(description="The Take Profit value used by the action.")
    stop_loss: Decimal = Field(description="The Stop Loss value used by the action.")
    status: bool = Field(default=True, description="Whether the action is active.")
    description: str | None = Field(default=None, description="Describes the action.")
