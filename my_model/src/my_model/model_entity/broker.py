"""Broker: a broker supported by the system, owned by a user, independent of any one Trading Platform."""

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from my_model.model_declaration import Model_Declaration


class Broker(Model_Declaration, table=True):
    __table_args__ = (UniqueConstraint("user_id", "name"),)

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    description: str | None = Field(default=None)
