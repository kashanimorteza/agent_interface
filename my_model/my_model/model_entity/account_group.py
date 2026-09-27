"""Account Group Domain Entity: an independent group for organizing trading accounts."""

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, UniqueConstraint

from my_model.model_declaration import Model_Declaration
from my_model.model_foundation import Model_Foundation

if TYPE_CHECKING:
    from my_model.model_entity.user import User


class AccountGroup(Model_Declaration, Model_Foundation, table=True):
    """An independent group for organizing trading accounts owned by one user."""

    __tablename__ = "account_group"
    __table_args__ = (UniqueConstraint("user_id", "name"),)

    user_id: int = Field(foreign_key="user.id", nullable=False)
    name: str = Field(nullable=False)

    user: "User" = Relationship()
