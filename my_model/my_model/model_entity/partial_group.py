"""Partial Group Domain Entity: an independent group of partial-close rules."""

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, UniqueConstraint

from my_model.model_declaration import Model_Declaration
from my_model.model_foundation import Model_Foundation

if TYPE_CHECKING:
    from my_model.model_entity.user import User


class PartialGroup(Model_Declaration, Model_Foundation, table=True):
    """An independent group of rules for managing portions of an open trade."""

    __tablename__ = "partial_group"
    __table_args__ = (UniqueConstraint("user_id", "name"),)

    user_id: int = Field(foreign_key="user.id", nullable=False)
    name: str = Field(nullable=False)

    user: "User" = Relationship()
