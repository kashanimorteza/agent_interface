"""Partial Rule: an individual rule telling the system when and how much of an open position must be closed."""

from decimal import Decimal

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from my_model.model_declaration import Model_Declaration


class PartialRule(Model_Declaration, table=True):
    __tablename__ = "partial_rule"
    __table_args__ = (UniqueConstraint("partial_group_id", "profit_percentage"),)

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True)
    partial_group_id: int = Field(foreign_key="partial_group.id", nullable=False)
    profit_percentage: Decimal = Field(nullable=False)
    close_percentage: Decimal = Field(nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    description: str | None = Field(default=None)
