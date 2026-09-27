"""Trailing Rule Domain Entity: one rule within a Trailing Group."""

from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, UniqueConstraint

from my_model.model_declaration import Model_Declaration
from my_model.model_foundation import Model_Foundation

if TYPE_CHECKING:
    from my_model.model_entity.trailing_group import TrailingGroup


class TrailingRule(Model_Declaration, Model_Foundation, table=True):
    """An individual rule within a Trailing Group telling the system when and how to adjust Take Profit and Stop Loss."""

    __tablename__ = "trailing_rule"
    __table_args__ = (UniqueConstraint("trailing_group_id", "trigger_percentage"),)

    name: str = Field(nullable=False, unique=True)
    trailing_group_id: int = Field(foreign_key="trailing_group.id", nullable=False)
    trigger_percentage: Decimal = Field(nullable=False)
    take_profit_adjustment: Optional[Decimal] = Field(default=None, nullable=True)
    stop_loss_adjustment: Optional[Decimal] = Field(default=None, nullable=True)

    trailing_group: "TrailingGroup" = Relationship()
