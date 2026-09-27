"""Action: defines how a position must be opened, bringing together asset, account, risk, and rule-group choices."""

from decimal import Decimal

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from my_model.model_declaration import Model_Declaration


class Action(Model_Declaration, table=True):
    __table_args__ = (UniqueConstraint("action_group_id", "name"),)

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    action_group_id: int = Field(foreign_key="action_group.id", nullable=False)
    asset_id: int = Field(foreign_key="asset.id", nullable=False)
    account_id: int = Field(foreign_key="account.id", nullable=False)
    partial_group_id: int = Field(foreign_key="partial_group.id", nullable=False)
    trailing_group_id: int = Field(foreign_key="trailing_group.id", nullable=False)
    risk_by_reward: Decimal = Field(nullable=False)
    take_profit: Decimal = Field(nullable=False)
    stop_loss: Decimal = Field(nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    description: str | None = Field(default=None)
