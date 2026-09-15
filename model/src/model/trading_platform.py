"""Domain Definition for Trading Platform."""

from __future__ import annotations

from pydantic import Field

from model.foundation import DomainModel


class TradingPlatform(DomainModel):
    """Defines a supported trading API standard while keeping the system independent of
    any specific exchange or broker.
    """

    __primary_key__ = ("id",)
    __auto_increment__ = ("id",)
    __unique__ = ("name",)
    __unique_sets__ = ()
    __foreign_keys__ = {}
    __credentials__ = {}

    id: int = Field(...)
    name: str = Field(...)
    code: str = Field(...)
    is_active: bool = Field(default=True)
    description: str | None = Field(default=None)
