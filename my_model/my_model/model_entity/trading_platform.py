"""Trading Platform Domain Entity: a supported trading API standard."""

from sqlmodel import Field

from my_model.model_declaration import Model_Declaration
from my_model.model_foundation import Model_Foundation


class TradingPlatform(Model_Declaration, Model_Foundation, table=True):
    """A supported trading platform, such as MetaTrader 5 or Binance."""

    __tablename__ = "trading_platform"

    name: str = Field(nullable=False, unique=True)
    code: str = Field(nullable=False)
