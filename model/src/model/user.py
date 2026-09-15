"""Domain Definition for User."""

from __future__ import annotations

from pydantic import Field

from model.foundation import Credential, DomainModel


class User(DomainModel):
    """Defines an independent user of the system and enables multi-user operation."""

    __primary_key__ = ("id",)
    __auto_increment__ = ("id",)
    __unique__ = ("name", "username")
    __unique_sets__ = ()
    __foreign_keys__ = {}
    __credentials__ = {"password": Credential.HASH, "api_key": Credential.HASH}

    id: int = Field(...)
    name: str = Field(...)
    username: str = Field(...)
    password: str = Field(...)
    api_key: str = Field(...)
    is_active: bool = Field(default=True)
    description: str | None = Field(default=None)
