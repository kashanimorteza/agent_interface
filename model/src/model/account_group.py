"""Domain Definition for Account Group."""

from __future__ import annotations

from pydantic import Field

from model.foundation import DomainModel, ForeignKey


class AccountGroup(DomainModel):
    """Defines an independent group for organizing trading accounts owned by one user."""

    __primary_key__ = ("id",)
    __auto_increment__ = ("id",)
    __unique__ = ()
    __unique_sets__ = (("user_id", "name"),)
    __foreign_keys__ = {"user_id": ForeignKey(target="User", field="id", cardinality="many_to_one")}
    __credentials__ = {}

    id: int = Field(...)
    user_id: int = Field(...)
    name: str = Field(...)
    is_active: bool = Field(default=True)
    description: str | None = Field(default=None)
