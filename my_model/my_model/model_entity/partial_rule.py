"""Partial Rule Domain Entity: one Partial Close rule within a Partial Group."""

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, UniqueConstraint

from my_model.model_declaration import Model_Declaration
from my_model.model_foundation import Model_Foundation

if TYPE_CHECKING:
    from my_model.model_entity.partial_group import PartialGroup


class PartialRule(Model_Declaration, Model_Foundation, table=True):
    """An individual Partial Close rule telling the system when and how much of an open position to close."""

    __tablename__ = "partial_rule"
    __table_args__ = (UniqueConstraint("partial_group_id", "profit_percentage"),)

    name: str = Field(nullable=False, unique=True)
    partial_group_id: int = Field(foreign_key="partial_group.id", nullable=False)
    profit_percentage: Decimal = Field(nullable=False)
    close_percentage: Decimal = Field(nullable=False)

    partial_group: "PartialGroup" = Relationship()
