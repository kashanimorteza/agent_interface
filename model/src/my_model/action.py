"""How a position must be opened: asset, account, risk, and rule-group selection."""

from __future__ import annotations

from decimal import Decimal
from typing import Any

from pydantic import Field

from ._base import DomainModel


class Action(DomainModel):
    """An action defining the asset, account, risk parameters, and rule groups for opening a position."""

    unique_together = (("action_group_id", "name"),)

    id: int | None = Field(default=None, description="Primary key, auto-incremented.")
    name: str = Field(description="The action's display name.")
    action_group_id: int = Field(description="Identifies the action group that contains the action.")
    asset_id: int = Field(description="Identifies the asset traded by the action.")
    account_id: int = Field(description="Identifies the account used to execute the action.")
    partial_group_id: int = Field(description="Identifies the Partial Group used by the action.")
    trailing_group_id: int = Field(description="Identifies the Trailing Group used by the action.")
    risk_by_reward: Decimal = Field(description="Defines the numeric risk-to-reward value used by the action.")
    take_profit: Decimal = Field(description="Defines the Take Profit value used by the action.")
    stop_loss: Decimal = Field(description="Defines the Stop Loss value used by the action.")
    status: bool = Field(default=True, description="Indicates whether the action is active.")
    description: str | None = Field(default=None, description="Describes the action.")


INITIAL_DATA: tuple[dict[str, Any], ...] = (
    {
        "name": "Default",
        "action_group_id": 1,
        "asset_id": 1,
        "account_id": 1,
        "partial_group_id": 1,
        "trailing_group_id": 1,
        "risk_by_reward": Decimal(1),
        "take_profit": Decimal(1),
        "stop_loss": Decimal(1),
    },
)
