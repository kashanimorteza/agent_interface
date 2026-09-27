"""Instance Domain Entity: a user-owned connection instance to a Trading Platform."""

from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, UniqueConstraint

from my_model.model_declaration import Model_Declaration
from my_model.model_foundation import Model_Foundation

if TYPE_CHECKING:
    from my_model.model_entity.trading_platform import TradingPlatform
    from my_model.model_entity.user import User


class Instance(Model_Declaration, Model_Foundation, table=True):
    """A user-owned connection instance through which the system accesses a Trading Platform."""

    __tablename__ = "instance"
    __table_args__ = (UniqueConstraint("user_id", "name"),)

    user_id: int = Field(foreign_key="user.id", nullable=False)
    trading_platform_id: int = Field(foreign_key="trading_platform.id", nullable=False)
    name: str = Field(nullable=False)
    ip: Optional[str] = Field(default=None, nullable=True)
    username: Optional[str] = Field(default=None, nullable=True)
    password: Optional[str] = Field(default=None, nullable=True, schema_extra={"sensitivity_marker": "password"})
    api_key: Optional[str] = Field(default=None, nullable=True, schema_extra={"sensitivity_marker": "password"})

    user: "User" = Relationship()
    trading_platform: "TradingPlatform" = Relationship()
