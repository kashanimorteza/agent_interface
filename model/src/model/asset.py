"""Domain Definition for Asset."""

from __future__ import annotations

from pydantic import Field

from model.foundation import DomainModel, ForeignKey


class Asset(DomainModel):
    """Defines an asset that can be selected for trading."""

    __primary_key__ = ("id",)
    __auto_increment__ = ("id",)
    __unique__ = ()
    __unique_sets__ = (("broker_id", "symbol"),)
    __foreign_keys__ = {
        "broker_id": ForeignKey(target="Broker", field="id", cardinality="many_to_one")
    }
    __credentials__ = {}

    id: int = Field(...)
    broker_id: int = Field(...)
    symbol: str = Field(...)
    category: str = Field(...)
    point_size: float = Field(default=0.0)
    digits: int = Field(default=0)
    is_active: bool = Field(default=True)
    description: str | None = Field(default=None)
