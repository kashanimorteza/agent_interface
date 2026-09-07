"""Action: how a position must be opened."""

from __future__ import annotations

from decimal import Decimal

from .account import Account
from .action_group import ActionGroup
from .asset import Asset
from .base import Model, Relationship, field
from .partial_group import PartialGroup
from .trailing_group import TrailingGroup


class Action(Model):
    """Defines how a position must be opened. An action selects the asset and
    account and provides the risk, Take Profit, Stop Loss, Partial Group, and
    Trailing Group settings that determine the position's parameters and
    execution behavior."""

    id: int | None = field("integer", primary_key=True, auto_increment=True)
    name: str = field("string", unique=True, purpose="The action's display name.")
    action_group_id: int = field(
        "integer", purpose="Identifies the action group that contains the action."
    )
    asset_id: int = field("integer", purpose="Identifies the asset traded by the action.")
    account_id: int = field("integer", purpose="Identifies the account used to execute the action.")
    partial_group_id: int = field(
        "integer", purpose="Identifies the Partial Group used by the action."
    )
    trailing_group_id: int = field(
        "integer", purpose="Identifies the Trailing Group used by the action."
    )
    risk_by_reward: Decimal = field(
        "decimal", purpose="Defines the numeric risk-to-reward value used by the action."
    )
    take_profit: Decimal = field(
        "decimal", purpose="Defines the Take Profit value used by the action."
    )
    stop_loss: Decimal = field("decimal", purpose="Defines the Stop Loss value used by the action.")
    status: bool = field("boolean", default=True, purpose="Indicates whether the action is active.")
    description: str | None = field("string", nullable=True, purpose="Describes the action.")

    relationships = (
        Relationship(field="action_group_id", target=ActionGroup, kind="belongs_to"),
        Relationship(field="asset_id", target=Asset, kind="uses"),
        Relationship(field="account_id", target=Account, kind="uses"),
        Relationship(field="partial_group_id", target=PartialGroup, kind="uses"),
        Relationship(field="trailing_group_id", target=TrailingGroup, kind="uses"),
    )

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
