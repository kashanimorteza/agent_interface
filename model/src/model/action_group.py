"""Action Group Domain Definition.

Represents an independent grouping for trading actions based on their
risk profile, owned by one User.
"""

from __future__ import annotations

from pydantic import Field

from model.foundation import DomainModel


class ActionGroup(DomainModel):
    """A group organizing Actions by risk profile, owned by one User."""

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
                "of": "ActionGroup",
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
