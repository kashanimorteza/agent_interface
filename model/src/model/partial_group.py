"""Partial Group Domain Definition.

Represents an independent group of rules for managing portions of an open
trade, owned by one User.
"""

from __future__ import annotations

from pydantic import Field

from model.foundation import DomainModel


class PartialGroup(DomainModel):
    """A group organizing Partial Rules owned by one User."""

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
                "of": "PartialGroup",
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
