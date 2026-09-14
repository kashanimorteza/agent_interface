"""The Broker Domain Definition."""

from __future__ import annotations

from typing import ClassVar

from .foundation import ModelBase, UniqueConstraints, identity_field


class Broker(ModelBase):
    """A broker supported by the system, owned by a user, independent of any one Trading Platform."""

    id: int = identity_field()
    name: str
    user_id: int
    status: bool = True
    description: str | None = None

    unique_constraints: ClassVar[UniqueConstraints] = (("user_id", "name"),)
