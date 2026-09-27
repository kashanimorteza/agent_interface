"""Currency Domain Entity: a currency usable by the trading system."""

from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, UniqueConstraint

from my_model.model_declaration import Model_Declaration
from my_model.model_foundation import Model_Foundation

if TYPE_CHECKING:
    from my_model.model_entity.user import User


class Currency(Model_Declaration, Model_Foundation, table=True):
    """A currency that can be used by the trading system, owned by a user."""

    __tablename__ = "currency"
    __table_args__ = (UniqueConstraint("user_id", "code"),)

    user_id: int = Field(foreign_key="user.id", nullable=False)
    code: str = Field(nullable=False, max_length=3)
    symbol: Optional[str] = Field(default=None, nullable=True)
    country: Optional[str] = Field(default=None, nullable=True)
    decimal_digits: int = Field(default=2, nullable=False)

    user: "User" = Relationship()
