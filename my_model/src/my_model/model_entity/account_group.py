"""Account Group: an independent group for organizing the trading accounts owned by one user."""

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from my_model.model_declaration import Model_Declaration


class AccountGroup(Model_Declaration, table=True):
    __tablename__ = "account_group"
    __table_args__ = (UniqueConstraint("user_id", "name"),)

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    name: str = Field(nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    description: str | None = Field(default=None)
