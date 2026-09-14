"""The User Domain Definition."""

from __future__ import annotations

from typing import ClassVar

from .foundation import ModelBase, UniqueConstraints, credential_field, identity_field


class User(ModelBase):
    """An independent user of the system, enabling multi-user operation."""

    id: int = identity_field()
    name: str
    username: str
    password: str = credential_field()
    api_key: str = credential_field()
    status: bool = True
    description: str | None = None

    unique_constraints: ClassVar[UniqueConstraints] = (("name",),)
