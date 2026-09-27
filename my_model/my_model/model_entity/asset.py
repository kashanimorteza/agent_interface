"""Asset Domain Entity: an asset that can be selected for trading."""

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, UniqueConstraint

from my_model.model_declaration import Model_Declaration
from my_model.model_foundation import Model_Foundation

if TYPE_CHECKING:
    from my_model.model_entity.broker import Broker


class Asset(Model_Declaration, Model_Foundation, table=True):
    """A tradable asset provided by a Broker."""

    __tablename__ = "asset"
    __table_args__ = (UniqueConstraint("broker_id", "symbol"),)

    broker_id: int = Field(foreign_key="broker.id", nullable=False)
    symbol: str = Field(nullable=False)
    category: str = Field(nullable=False)
    point_size: float = Field(default=0.0, nullable=False)
    digits: int = Field(default=0, nullable=False)

    broker: "Broker" = Relationship()
