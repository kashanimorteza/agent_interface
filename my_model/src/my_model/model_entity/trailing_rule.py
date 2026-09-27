"""Trailing Rule: an individual rule within a Trailing Group telling the system when and how to manage Take Profit and Stop Loss."""

from decimal import Decimal

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from my_model.model_declaration import Model_Declaration


class TrailingRule(Model_Declaration, table=True):
    __tablename__ = "trailing_rule"
    __table_args__ = (UniqueConstraint("trailing_group_id", "trigger_percentage"),)

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True)
    trailing_group_id: int = Field(foreign_key="trailing_group.id", nullable=False)
    trigger_percentage: Decimal = Field(nullable=False)
    take_profit_adjustment: Decimal | None = Field(default=None)
    stop_loss_adjustment: Decimal | None = Field(default=None)
    is_active: bool = Field(default=True, nullable=False)
    description: str | None = Field(default=None)
