"""Action Domain Entity: defines how a position must be opened."""

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, UniqueConstraint

from my_model.model_declaration import Model_Declaration
from my_model.model_foundation import Model_Foundation

if TYPE_CHECKING:
    from my_model.model_entity.account import Account
    from my_model.model_entity.action_group import ActionGroup
    from my_model.model_entity.asset import Asset
    from my_model.model_entity.partial_group import PartialGroup
    from my_model.model_entity.trailing_group import TrailingGroup


class Action(Model_Declaration, Model_Foundation, table=True):
    """How a position must be opened: asset, account, risk, Take Profit, Stop Loss, and rule groups."""

    __tablename__ = "action"
    __table_args__ = (UniqueConstraint("action_group_id", "name"),)

    name: str = Field(nullable=False)
    action_group_id: int = Field(foreign_key="action_group.id", nullable=False)
    asset_id: int = Field(foreign_key="asset.id", nullable=False)
    account_id: int = Field(foreign_key="account.id", nullable=False)
    partial_group_id: int = Field(foreign_key="partial_group.id", nullable=False)
    trailing_group_id: int = Field(foreign_key="trailing_group.id", nullable=False)
    risk_by_reward: Decimal = Field(nullable=False)
    take_profit: Decimal = Field(nullable=False)
    stop_loss: Decimal = Field(nullable=False)

    action_group: "ActionGroup" = Relationship()
    asset: "Asset" = Relationship()
    account: "Account" = Relationship()
    partial_group: "PartialGroup" = Relationship()
    trailing_group: "TrailingGroup" = Relationship()
