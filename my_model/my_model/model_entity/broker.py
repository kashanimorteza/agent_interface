"""Broker Domain Entity: a broker supported by the system."""

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, UniqueConstraint

from my_model.model_declaration import Model_Declaration
from my_model.model_foundation import Model_Foundation

if TYPE_CHECKING:
    from my_model.model_entity.user import User


class Broker(Model_Declaration, Model_Foundation, table=True):
    """A broker supported by the system, owned by the user who configures it."""

    __tablename__ = "broker"
    __table_args__ = (UniqueConstraint("user_id", "name"),)

    name: str = Field(nullable=False)
    user_id: int = Field(foreign_key="user.id", nullable=False)

    user: "User" = Relationship()
