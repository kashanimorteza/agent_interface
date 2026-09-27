"""Trading Platform: a supported trading API standard, kept independent of any specific exchange or broker."""

from sqlmodel import Field

from my_model.model_declaration import Model_Declaration


class TradingPlatform(Model_Declaration, table=True):
    __tablename__ = "trading_platform"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True)
    code: str = Field(nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    description: str | None = Field(default=None)
