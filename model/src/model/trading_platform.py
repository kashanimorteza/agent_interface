"""The Trading Platform Domain Definition."""

from __future__ import annotations

from .foundation import ModelBase, identity_field


class TradingPlatform(ModelBase):
    """A supported trading API standard, independent of any specific exchange or broker."""

    id: int = identity_field()
    name: str
    code: str
    status: bool = True
    description: str | None = None
