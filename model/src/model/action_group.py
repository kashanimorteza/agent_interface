"""The Action Group Domain Definition."""

from __future__ import annotations

from typing import ClassVar

from .foundation import ModelBase, UniqueConstraints, identity_field


class ActionGroup(ModelBase):
    """An independent grouping for trading actions based on their risk profile."""

    id: int = identity_field()
    user_id: int
    name: str
    status: bool = True
    description: str | None = None

    unique_constraints: ClassVar[UniqueConstraints] = (("user_id", "name"),)
