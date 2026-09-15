"""Domain Definition for Instance."""

from __future__ import annotations

from pydantic import Field

from model.foundation import Credential, DomainModel, ForeignKey


class Instance(DomainModel):
    """Defines a user-owned connection instance through which the system accesses a
    supported Trading Platform.
    """

    __primary_key__ = ("id",)
    __auto_increment__ = ("id",)
    __unique__ = ()
    __unique_sets__ = (("user_id", "name"),)
    __foreign_keys__ = {
        "user_id": ForeignKey(target="User", field="id", cardinality="many_to_one"),
        "trading_platform_id": ForeignKey(
            target="TradingPlatform", field="id", cardinality="many_to_one"
        ),
    }
    __credentials__ = {"password": Credential.ENCRYPTED, "api_key": Credential.ENCRYPTED}

    id: int = Field(...)
    user_id: int = Field(...)
    trading_platform_id: int = Field(...)
    name: str = Field(...)
    ip: str | None = Field(default=None)
    username: str | None = Field(default=None)
    password: str | None = Field(default=None)
    api_key: str | None = Field(default=None)
    is_active: bool = Field(default=True)
    description: str | None = Field(default=None)
