"""The Action domain Model: how a position must be opened."""

from decimal import Decimal

from pydantic import Field

from ._base import BaseModel


class Action(BaseModel):
    """Defines how a position must be opened.

    An action selects the asset and account and provides the risk, Take
    Profit, Stop Loss, Partial Group, and Trailing Group settings that
    determine the position's parameters and execution behavior. The
    combination-uniqueness of `action_group_id` and `name` is a domain rule
    traceable to this Model, enforced by Database.
    """

    id: int | None = Field(default=None, description="The action's generated identity.")
    name: str = Field(description="The action's display name.")
    action_group_id: int = Field(description="Identifies the action group that contains the action.")
    asset_id: int = Field(description="Identifies the asset traded by the action.")
    account_id: int = Field(description="Identifies the account used to execute the action.")
    partial_group_id: int = Field(description="Identifies the Partial Group used by the action.")
    trailing_group_id: int = Field(description="Identifies the Trailing Group used by the action.")
    risk_by_reward: Decimal = Field(
        description="Defines the numeric risk-to-reward value used by the action."
    )
    take_profit: Decimal = Field(description="Defines the Take Profit value used by the action.")
    stop_loss: Decimal = Field(description="Defines the Stop Loss value used by the action.")
    status: bool = Field(default=True, description="Indicates whether the action is active.")
    description: str | None = Field(default=None, description="Describes the action.")


INITIAL_DATA: list[dict[str, object]] = [
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
]
