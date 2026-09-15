"""Domain Definition for Currency."""

from __future__ import annotations

from pydantic import Field

from model.foundation import DomainModel, ForeignKey


class Currency(DomainModel):
    """Defines a currency that can be used by the trading system."""

    __primary_key__ = ("id",)
    __auto_increment__ = ("id",)
    __unique__ = ()
    __unique_sets__ = (("user_id", "code"),)
    __foreign_keys__ = {"user_id": ForeignKey(target="User", field="id", cardinality="many_to_one")}
    __credentials__ = {}

    id: int = Field(...)
    user_id: int = Field(...)
    code: str = Field(..., max_length=3)
    symbol: str | None = Field(default=None)
    country: str | None = Field(default=None)
    decimal_digits: int = Field(default=2)
    is_active: bool = Field(default=True)
    description: str | None = Field(default=None)
