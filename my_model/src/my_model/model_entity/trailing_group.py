"""Trailing Group: an independent group organizing the rules that manage Stop Loss and Take Profit during a trade."""

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from my_model.model_declaration import Model_Declaration


class TrailingGroup(Model_Declaration, table=True):
    __tablename__ = "trailing_group"
    __table_args__ = (UniqueConstraint("user_id", "name"),)

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    name: str = Field(nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    description: str | None = Field(default=None)
