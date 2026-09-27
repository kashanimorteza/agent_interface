"""Instance: a user-owned connection instance through which the system accesses a supported Trading Platform."""

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from my_model.model_declaration import Model_Declaration


class Instance(Model_Declaration, table=True):
    __table_args__ = (UniqueConstraint("user_id", "name"),)

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    trading_platform_id: int = Field(foreign_key="trading_platform.id", nullable=False)
    name: str = Field(nullable=False)
    ip: str | None = Field(default=None)
    username: str | None = Field(default=None)
    password: str | None = Field(default=None, schema_extra={"sensitivity": "password"})
    api_key: str | None = Field(default=None, schema_extra={"sensitivity": "sensitive"})
    is_active: bool = Field(default=True, nullable=False)
    description: str | None = Field(default=None)
