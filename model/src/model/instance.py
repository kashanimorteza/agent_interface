"""The Instance Domain Definition."""

from __future__ import annotations

from typing import ClassVar

from .foundation import ModelBase, UniqueConstraints, credential_field, identity_field


class Instance(ModelBase):
    """A user-owned connection instance through which the system accesses a Trading Platform."""

    id: int = identity_field()
    user_id: int
    name: str
    trading_platform_id: int
    ip: str | None = None
    username: str | None = None
    password: str | None = credential_field(default=None)
    api_key: str | None = credential_field(default=None)
    status: bool = True
    description: str | None = None

    unique_constraints: ClassVar[UniqueConstraints] = (("user_id", "name"),)
