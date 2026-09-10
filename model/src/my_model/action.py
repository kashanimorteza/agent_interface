from __future__ import annotations

from decimal import Decimal
from typing import ClassVar

from pydantic import Field

from ._base import DomainModel
from ._shared import Relationship


class Action(DomainModel):
    name: str = Field(..., description="The action's display name.")
    action_group_id: int = Field(..., description="Identifies the action group that contains the action.")
    asset_id: int = Field(..., description="Identifies the asset traded by the action.")
    account_id: int = Field(..., description="Identifies the account used to execute the action.")
    partial_group_id: int = Field(..., description="Identifies the Partial Group used by the action.")
    trailing_group_id: int = Field(..., description="Identifies the Trailing Group used by the action.")
    risk_by_reward: Decimal = Field(
        ..., description="Defines the numeric risk-to-reward value used by the action."
    )
    take_profit: Decimal = Field(..., description="Defines the Take Profit value used by the action.")
    stop_loss: Decimal = Field(..., description="Defines the Stop Loss value used by the action.")
    status: bool = Field(default=True, description="Indicates whether the action is active.")
    description: str | None = Field(default=None, description="Describes the action.")

    unique_together: ClassVar[list[tuple[str, ...]]] = [("action_group_id", "name")]
    relationships: ClassVar[dict[str, Relationship]] = {
        "action_group": Relationship(target="ActionGroup", cardinality="one", field="action_group_id"),
        "asset": Relationship(target="Asset", cardinality="one", field="asset_id"),
        "account": Relationship(target="Account", cardinality="one", field="account_id"),
        "partial_group": Relationship(target="PartialGroup", cardinality="one", field="partial_group_id"),
        "trailing_group": Relationship(
            target="TrailingGroup", cardinality="one", field="trailing_group_id"
        ),
    }


ACTION_INITIAL_DATA: list[dict] = [
    {
        "name": "Default",
        "action_group_id": 1,
        "asset_id": 1,
        "account_id": 1,
        "partial_group_id": 1,
        "trailing_group_id": 1,
        "risk_by_reward": 1,
        "take_profit": 1,
        "stop_loss": 1,
    },
]
