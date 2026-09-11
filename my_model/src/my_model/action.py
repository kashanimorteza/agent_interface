from decimal import Decimal

from pydantic import Field

from ._base import BaseModel


class Action(BaseModel):
    """Defines how a position must be opened: the asset, account, risk, and rule sets that determine its parameters."""

    id: int | None = Field(
        default=None, description="Generated once the Action is persisted."
    )
    name: str = Field(description="The action's display name.")
    action_group_id: int = Field(
        description="Identifies the action group that contains the action."
    )
    asset_id: int = Field(description="Identifies the asset traded by the action.")
    account_id: int = Field(
        description="Identifies the account used to execute the action."
    )
    partial_group_id: int = Field(
        description="Identifies the Partial Group used by the action."
    )
    trailing_group_id: int = Field(
        description="Identifies the Trailing Group used by the action."
    )
    risk_by_reward: Decimal = Field(
        description="The numeric risk-to-reward value used by the action."
    )
    take_profit: Decimal = Field(
        description="The Take Profit value used by the action."
    )
    stop_loss: Decimal = Field(description="The Stop Loss value used by the action.")
    status: bool = Field(
        default=True, description="Indicates whether the action is active."
    )
    description: str | None = Field(default=None, description="Describes the action.")
