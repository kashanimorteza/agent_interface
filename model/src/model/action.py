"""The Action Domain Definition."""

from __future__ import annotations

from decimal import Decimal
from typing import ClassVar

from model.foundation import ModelBase, persistence_field


class Action(ModelBase):
    """How a position must be opened.

    Selects the asset and account and provides the risk, Take Profit, Stop
    Loss, Partial Group, and Trailing Group settings that determine the
    position's parameters and execution behavior.
    """

    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (("action_group_id", "name"),)

    id: int = persistence_field(
        primary_key=True,
        auto_increment=True,
        description="Primary identity of the action.",
    )
    name: str = persistence_field(description="The action's display name.")
    action_group_id: int = persistence_field(
        foreign_key="action_group.id",
        description="Identifies the action group that contains the action.",
    )
    asset_id: int = persistence_field(
        foreign_key="asset.id", description="Identifies the asset traded by the action."
    )
    account_id: int = persistence_field(
        foreign_key="account.id",
        description="Identifies the account used to execute the action.",
    )
    partial_group_id: int = persistence_field(
        foreign_key="partial_group.id",
        description="Identifies the Partial Group used by the action.",
    )
    trailing_group_id: int = persistence_field(
        foreign_key="trailing_group.id",
        description="Identifies the Trailing Group used by the action.",
    )
    risk_by_reward: Decimal = persistence_field(
        description="Defines the numeric risk-to-reward value used by the action."
    )
    take_profit: Decimal = persistence_field(
        description="Defines the Take Profit value used by the action."
    )
    stop_loss: Decimal = persistence_field(
        description="Defines the Stop Loss value used by the action."
    )
    is_active: bool = persistence_field(
        default=True, description="Indicates whether the action is active."
    )
    description: str | None = persistence_field(
        default=None, description="Describes the action."
    )
