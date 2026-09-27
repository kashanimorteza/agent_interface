"""Trailing Group Domain Entity: an independent group of Stop Loss / Take Profit rules."""

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, UniqueConstraint

from my_model.model_declaration import Model_Declaration
from my_model.model_foundation import Model_Foundation

if TYPE_CHECKING:
    from my_model.model_entity.user import User


class TrailingGroup(Model_Declaration, Model_Foundation, table=True):
    """An independent group for organizing the rules that manage Stop Loss and Take Profit."""

    __tablename__ = "trailing_group"
    __table_args__ = (UniqueConstraint("user_id", "name"),)

    user_id: int = Field(foreign_key="user.id", nullable=False)
    name: str = Field(nullable=False)

    user: "User" = Relationship()
