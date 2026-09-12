"""The Instance domain entity: a user's connection to a Trading Platform."""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import Field

from my_model._base import BaseModel
from my_model._initial_data import GENERATE_SECURELY


class Instance(BaseModel):
    """A user-owned connection instance through which the system accesses a
    supported Trading Platform.

    The Trading Platform selected through ``trading_platform_id`` defines
    which connection fields are required; every field it requires must be
    present before the Instance can be used. That platform-specific
    requirement is resolved from the Trading Platform's own definition, not
    hardcoded here.
    """

    UNIQUE_TOGETHER: ClassVar[tuple[tuple[str, ...], ...]] = (("user_id", "name"),)
    INITIAL_DATA: ClassVar[tuple[dict[str, Any], ...]] = (
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

    id: int | None = Field(
        default=None,
        description="Assigned by generation before the record is considered complete.",
    )
    user_id: int = Field(description="Identifies the user who owns this instance.")
    name: str = Field(description="The instance's display name.")
    trading_platform_id: int = Field(
        description="Identifies the trading platform used by this instance."
    )
    ip: str | None = Field(
        default=None,
        description="Identifies the technical network address used to reach the Trading Platform when required.",
    )
    username: str | None = Field(
        default=None,
        description="Defines the technical username used to establish the Instance connection when required.",
    )
    password: str | None = Field(
        default=None,
        repr=False,
        json_schema_extra={"credential": True, "storage_at_rest": "encrypted"},
        description="Defines the technical password used to establish the Instance connection when required.",
    )
    api_key: str | None = Field(
        default=None,
        repr=False,
        json_schema_extra={"credential": True, "storage_at_rest": "encrypted"},
        description="Defines the technical API credential used to establish the Instance connection when required.",
    )
    status: bool = Field(
        default=True, description="Indicates whether the instance is active."
    )
    description: str | None = Field(default=None, description="Describes the instance.")

    def missing_required_connection_fields(
        self, required_fields: tuple[str, ...]
    ) -> tuple[str, ...]:
        """Return which of the platform-required connection fields are absent.

        ``required_fields`` names the connection fields the selected Trading
        Platform requires; this Instance does not know that requirement on
        its own, so the caller resolves it from the Trading Platform first.
        """
        return tuple(
            field for field in required_fields if getattr(self, field, None) is None
        )
