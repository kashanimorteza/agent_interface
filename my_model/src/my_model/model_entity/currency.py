"""Currency: a currency usable by the trading system, with its standard code, symbol, region, and monetary precision."""

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from my_model.model_declaration import Model_Declaration


class Currency(Model_Declaration, table=True):
    __table_args__ = (UniqueConstraint("user_id", "code"),)

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    code: str = Field(nullable=False, max_length=3)
    symbol: str | None = Field(default=None)
    country: str | None = Field(default=None)
    decimal_digits: int = Field(default=2, nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    description: str | None = Field(default=None)
