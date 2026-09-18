"""User Domain Definition.

Represents an independent user of the system and enables multi-user
operation. Every other user-owned Domain Definition references one
authoritative User identity.
"""

from __future__ import annotations

from pydantic import Field

from model.foundation import DomainModel


class User(DomainModel):
    """An independent user of the system."""

    persistent = True
    unique_sets = (("name",), ("username",))

    id: int | None = Field(
        default=None,
        json_schema_extra={
            "type": "integer",
            "primary_key": True,
            "auto_increment": True,
            "nullable": False,
        },
    )
    name: str = Field(
        json_schema_extra={"type": "string", "nullable": False, "unique": True},
    )
    username: str = Field(
        json_schema_extra={"type": "string", "nullable": False, "unique": True},
    )
    password: str = Field(
        json_schema_extra={
            "type": "string",
            "nullable": False,
            "credential": "hash",
        },
    )
    api_key: str = Field(
        json_schema_extra={
            "type": "string",
            "nullable": False,
            "credential": "hash",
        },
    )
    is_active: bool = Field(
        default=True,
        json_schema_extra={"type": "boolean", "nullable": False, "default": True},
    )
    description: str | None = Field(
        default=None,
        json_schema_extra={"type": "string", "nullable": True},
    )
