"""Action Entity."""

from decimal import Decimal

from model.declaration import Declaration
from model.entity.account import Account
from model.entity.action_group import ActionGroup
from model.entity.asset import Asset
from model.entity.partial_group import PartialGroup
from model.entity.trailing_group import TrailingGroup
from model.foundation import Foundation


class Action(Foundation, table=True):
    """Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior."""

    id: int | None = Declaration.identity()
    name: str = Declaration.field(description="The action's display name.")
    action_group_id: int = Declaration.field(
        reference=ActionGroup,
        description="Identifies the action group that contains the action.",
    )
    asset_id: int = Declaration.field(
        reference=Asset, description="Identifies the asset traded by the action."
    )
    account_id: int = Declaration.field(
        reference=Account,
        description="Identifies the account used to execute the action.",
    )
    partial_group_id: int = Declaration.field(
        reference=PartialGroup,
        description="Identifies the Partial Group used by the action.",
    )
    trailing_group_id: int = Declaration.field(
        reference=TrailingGroup,
        description="Identifies the Trailing Group used by the action.",
    )
    risk_by_reward: Decimal = Declaration.field(
        description="Defines the numeric risk-to-reward value used by the action."
    )
    take_profit: Decimal = Declaration.field(
        description="Defines the Take Profit value used by the action."
    )
    stop_loss: Decimal = Declaration.field(
        description="Defines the Stop Loss value used by the action."
    )
    is_active: bool = Declaration.field(
        default=True, description="Indicates whether the action is active."
    )
    description: str | None = Declaration.field(
        nullable=True, description="Describes the action."
    )

    __table_args__ = Declaration.composite(
        "Action", unique=(("action_group_id", "name"),)
    )
