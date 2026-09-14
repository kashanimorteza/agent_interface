"""The Trailing Group Domain Definition."""

from __future__ import annotations

from typing import ClassVar

from .foundation import ModelBase, UniqueConstraints, identity_field


class TrailingGroup(ModelBase):
    """An independent group for organizing rules that manage Stop Loss and Take Profit during a trade."""

    id: int = identity_field()
    user_id: int
    name: str
    status: bool = True
    description: str | None = None

    unique_constraints: ClassVar[UniqueConstraints] = (("user_id", "name"),)
