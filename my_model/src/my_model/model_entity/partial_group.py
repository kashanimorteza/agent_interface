"""Partial Group: an independent group of rules for managing partial closing of an open trade."""

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from my_model.model_declaration import Model_Declaration


class PartialGroup(Model_Declaration, table=True):
    __tablename__ = "partial_group"
    __table_args__ = (UniqueConstraint("user_id", "name"),)

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    name: str = Field(nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    description: str | None = Field(default=None)
