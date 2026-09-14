"""The Action Domain Definition."""

from __future__ import annotations

from decimal import Decimal
from typing import ClassVar

from .foundation import ModelBase, UniqueConstraints, identity_field


class Action(ModelBase):
    """How a position must be opened: selects the asset and account and provides its execution settings."""

    id: int = identity_field()
    name: str
    action_group_id: int
    asset_id: int
    account_id: int
    partial_group_id: int
    trailing_group_id: int
    risk_by_reward: Decimal
    take_profit: Decimal
    stop_loss: Decimal
    status: bool = True
    description: str | None = None

    unique_constraints: ClassVar[UniqueConstraints] = (("action_group_id", "name"),)
