"""Trailing Group Domain Definition.

Represents an independent group for organizing the rules that manage Stop
Loss and Take Profit during a trade, owned by one User.
"""

from __future__ import annotations

from pydantic import Field

from model.foundation import DomainModel


class TrailingGroup(DomainModel):
    """A group organizing Trailing Rules owned by one User."""

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
                "of": "TrailingGroup",
                "to": "User",
                "multiplicity": "many-to-one",
                "optional": False,
            },
        },
    )
    name: str = Field(
        json_schema_extra={"type": "string", "nullable": False},
    )
    is_active: bool = Field(
        default=True,
        json_schema_extra={"type": "boolean", "nullable": False, "default": True},
    )
    description: str | None = Field(
        default=None,
        json_schema_extra={"type": "string", "nullable": True},
    )
