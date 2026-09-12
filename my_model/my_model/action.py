"""The Action domain entity."""

from decimal import Decimal

from pydantic import Field

from my_model._base import BaseModel


class Action(BaseModel):
    """Defines how a position must be opened: selects the asset and account
    and provides the risk, Take Profit, Stop Loss, Partial Group, and
    Trailing Group settings that determine the position's parameters and
    execution behavior.
    """

    id: int = Field(description="The action's logical identity.")
    name: str = Field(description="The action's display name.")
    action_group_id: int = Field(description="Identifies the action group that contains the action.")
    asset_id: int = Field(description="Identifies the asset traded by the action.")
    account_id: int = Field(description="Identifies the account used to execute the action.")
    partial_group_id: int = Field(description="Identifies the Partial Group used by the action.")
    trailing_group_id: int = Field(description="Identifies the Trailing Group used by the action.")
    risk_by_reward: Decimal = Field(description="The numeric risk-to-reward value used by the action.")
    take_profit: Decimal = Field(description="The Take Profit value used by the action.")
    stop_loss: Decimal = Field(description="The Stop Loss value used by the action.")
    status: bool = Field(default=True, description="Whether the action is active.")
    description: str | None = Field(default=None, description="Describes the action.")


INITIAL_DATA: list[dict[str, object]] = [
    {
        "name": "Default",
        "action_group_id": 1,
        "asset_id": 1,
        "account_id": 1,
        "partial_group_id": 1,
        "trailing_group_id": 1,
        "risk_by_reward": "1",
        "take_profit": "1",
        "stop_loss": "1",
    },
]
