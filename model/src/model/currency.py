"""The Currency Domain Definition."""

from __future__ import annotations

from typing import ClassVar

from pydantic import Field

from .foundation import ModelBase, UniqueConstraints, identity_field


class Currency(ModelBase):
    """A currency usable by the trading system, with its standard code, symbol, and precision."""

    id: int = identity_field()
    user_id: int
    code: str = Field(min_length=3, max_length=3)
    symbol: str | None = None
    country: str | None = None
    decimal_digits: int = 2
    status: bool = True
    description: str | None = None

    unique_constraints: ClassVar[UniqueConstraints] = (("user_id", "code"),)
