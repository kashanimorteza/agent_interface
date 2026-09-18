"""Instance Domain Definition.

Represents a user-owned connection instance through which the system
accesses one supported Trading Platform. Which technical connection
fields (ip, username, password, api_key) a particular Instance actually
needs depends on the referenced Trading Platform's own requirements; that
dependency requires external, operation-specific context beyond this
Domain Definition's own data and is therefore not an Intrinsic Rule Model
enforces — it is realized by a Component with access to that context.
"""

from __future__ import annotations

from pydantic import Field

from model.foundation import DomainModel


class Instance(DomainModel):
    """A user-owned connection instance to one Trading Platform."""

    persistent = True
    unique_sets = (("user_id", "name"),)

    id: int | None = Field(
        default=None,
        json_schema_extra={
            "type": "integer",
            "primary_key": True,
            "auto_increment": True,
            "nullable": False,
        },
    )
    user_id: int = Field(
        json_schema_extra={
            "type": "integer",
            "nullable": False,
            "foreign_key": {"references": "User", "field": "id"},
            "cardinality": {
                "of": "Instance",
                "to": "User",
                "multiplicity": "many-to-one",
                "optional": False,
            },
        },
    )
    trading_platform_id: int = Field(
        json_schema_extra={
            "type": "integer",
            "nullable": False,
            "foreign_key": {"references": "TradingPlatform", "field": "id"},
            "cardinality": {
                "of": "Instance",
                "to": "TradingPlatform",
                "multiplicity": "many-to-one",
                "optional": False,
            },
        },
    )
    name: str = Field(
        json_schema_extra={"type": "string", "nullable": False},
    )
    ip: str | None = Field(
        default=None,
        json_schema_extra={"type": "string", "nullable": True},
    )
    username: str | None = Field(
        default=None,
        json_schema_extra={"type": "string", "nullable": True},
    )
    password: str | None = Field(
        default=None,
        json_schema_extra={
            "type": "string",
            "nullable": True,
            "credential": "encrypted",
        },
    )
    api_key: str | None = Field(
        default=None,
        json_schema_extra={
            "type": "string",
            "nullable": True,
            "credential": "encrypted",
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
