"""The Instance Domain Definition."""

from __future__ import annotations

from pydantic import Field

from .foundation import ModelBase


class Instance(ModelBase):
    """A user-owned connection instance through which the system accesses a Trading Platform."""

    UNIQUE_CONSTRAINTS = (("user_id", "name"),)

    id: int | None = Field(default=None, description="Auto-incrementing primary key.")
    user_id: int = Field(..., description="Identifies the user who owns this instance.")
    name: str = Field(..., description="The instance's display name.")
    trading_platform_id: int = Field(
        ..., description="Identifies the trading platform used by this instance."
    )
    ip: str | None = Field(
        default=None,
        description="Identifies the technical network address used to reach the "
        "Trading Platform when required.",
    )
    username: str | None = Field(
        default=None,
        description="Defines the technical username used to establish the Instance "
        "connection when required.",
    )
    password: str | None = Field(
        default=None,
        json_schema_extra={"credential": True},
        description="Defines the technical password used to establish the Instance "
        "connection when required.",
    )
    api_key: str | None = Field(
        default=None,
        json_schema_extra={"credential": True},
        description="Defines the technical API credential used to establish the Instance "
        "connection when required.",
    )
    is_active: bool = Field(default=True, description="Whether the instance is active.")
    description: str | None = Field(default=None, description="Describes the instance.")
