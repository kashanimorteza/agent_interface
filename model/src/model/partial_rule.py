"""The Partial Rule Domain Definition."""

from __future__ import annotations

from decimal import Decimal
from typing import ClassVar

from .foundation import ModelBase, UniqueConstraints, identity_field


class PartialRule(ModelBase):
    """One rule telling the system under which condition part of an open position must be closed."""

    id: int = identity_field()
    name: str
    partial_group_id: int
    profit_percentage: Decimal
    close_percentage: Decimal
    status: bool = True
    description: str | None = None

    unique_constraints: ClassVar[UniqueConstraints] = (
        ("name",),
        ("partial_group_id", "profit_percentage"),
    )
