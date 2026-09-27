"""Position: stores the complete information for every position the system creates, opened or still pending execution."""

from datetime import datetime
from decimal import Decimal

from sqlmodel import Field

from my_model.model_declaration import Model_Declaration


class Position(Model_Declaration, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    name: str = Field(nullable=False, unique=True)
    trading_platform_id: int = Field(foreign_key="trading_platform.id", nullable=False)
    broker_id: int = Field(foreign_key="broker.id", nullable=False)
    account_id: int = Field(foreign_key="account.id", nullable=False)
    trailing_group_id: int = Field(foreign_key="trailing_group.id", nullable=False)
    partial_group_id: int = Field(foreign_key="partial_group.id", nullable=False)
    action_group_id: int = Field(foreign_key="action_group.id", nullable=False)
    action_id: int = Field(foreign_key="action.id", nullable=False)
    date: datetime = Field(nullable=False)
    volume: Decimal = Field(nullable=False)
    profit: Decimal = Field(default=Decimal("0"), nullable=False)
    is_executed: bool = Field(default=False, nullable=False)
    order_type: str = Field(nullable=False)
    base_tp: Decimal = Field(nullable=False)
    base_sl: Decimal = Field(nullable=False)
    real_tp: Decimal = Field(nullable=False)
    real_sl: Decimal = Field(nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    description: str | None = Field(default=None)
