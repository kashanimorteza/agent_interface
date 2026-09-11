"""A user-owned connection instance through which the system accesses a Trading Platform."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from ._base import DomainModel, credential_field
from ._generation import GENERATE_SECURELY


class Instance(DomainModel):
    """A connection instance owned by one User, using one Trading Platform.

    The Trading Platform selected through ``trading_platform_id`` determines
    which of the technical connection fields (``ip``, ``username``,
    ``password``, ``api_key``) are required before the Instance can be used;
    that requirement is evaluated against the referenced Trading Platform at
    the point of use rather than declared as a fixed constraint here.
    """

    unique_together = (("user_id", "name"),)

    id: int | None = Field(default=None, description="Primary key, auto-incremented.")
    user_id: int = Field(description="Identifies the user who owns this instance.")
    name: str = Field(description="The instance's display name.")
    trading_platform_id: int = Field(description="Identifies the trading platform used by this instance.")
    ip: str | None = Field(
        default=None, description="The technical network address used to reach the Trading Platform when required."
    )
    username: str | None = Field(
        default=None, description="The technical username used to establish the Instance connection when required."
    )
    password: str | None = credential_field(
        default=None, description="The technical password used to establish the Instance connection when required."
    )
    api_key: str | None = credential_field(
        default=None, description="The technical API credential used to establish the Instance connection when required."
    )
    status: bool = Field(default=True, description="Indicates whether the instance is active.")
    description: str | None = Field(default=None, description="Describes the instance.")


INITIAL_DATA: tuple[dict[str, Any], ...] = (
    {
        "name": "MetaTrader",
        "user_id": 1,
        "trading_platform_id": 1,
        "ip": "127.0.0.1",
        "username": "test",
        "password": GENERATE_SECURELY,
        "api_key": GENERATE_SECURELY,
    },
)
