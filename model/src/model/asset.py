"""The Asset Domain Definition."""

from __future__ import annotations

from typing import ClassVar

from .foundation import ModelBase, UniqueConstraints, identity_field


class Asset(ModelBase):
    """An asset that can be selected for trading, provided by one Broker."""

    id: int = identity_field()
    broker_id: int
    symbol: str
    category: str
    point_size: float = 0.0
    digits: int = 0
    status: bool = True
    description: str | None = None

    unique_constraints: ClassVar[UniqueConstraints] = (("broker_id", "symbol"),)
