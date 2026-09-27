"""Asset: an asset that can be selected for trading, provided by a Broker."""

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from my_model.model_declaration import Model_Declaration


class Asset(Model_Declaration, table=True):
    __table_args__ = (UniqueConstraint("broker_id", "symbol"),)

    id: int | None = Field(default=None, primary_key=True)
    broker_id: int = Field(foreign_key="broker.id", nullable=False)
    symbol: str = Field(nullable=False)
    category: str = Field(nullable=False)
    point_size: float = Field(default=0.0, nullable=False)
    digits: int = Field(default=0, nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    description: str | None = Field(default=None)
