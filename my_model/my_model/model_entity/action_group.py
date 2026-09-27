"""Action Group Domain Entity: an independent grouping of trading actions by risk profile."""

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, UniqueConstraint

from my_model.model_declaration import Model_Declaration
from my_model.model_foundation import Model_Foundation

if TYPE_CHECKING:
    from my_model.model_entity.user import User


class ActionGroup(Model_Declaration, Model_Foundation, table=True):
    """An independent grouping for trading actions based on their risk profile."""

    __tablename__ = "action_group"
    __table_args__ = (UniqueConstraint("user_id", "name"),)

    user_id: int = Field(foreign_key="user.id", nullable=False)
    name: str = Field(nullable=False)

    user: "User" = Relationship()
