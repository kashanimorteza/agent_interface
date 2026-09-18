"""Asset Domain Definition.

Represents a tradable asset provided by one Broker, giving the system the
complete set of available tradable assets and their category.
"""

from __future__ import annotations

from pydantic import Field

from model.foundation import DomainModel


class Asset(DomainModel):
    """A tradable asset provided by one Broker."""

    persistent = True
    unique_sets = (("broker_id", "symbol"),)

    id: int | None = Field(
        default=None,
        json_schema_extra={
            "type": "integer",
            "primary_key": True,
            "auto_increment": True,
            "nullable": False,
        },
    )
    broker_id: int = Field(
        json_schema_extra={
            "type": "integer",
            "nullable": False,
            "foreign_key": {"references": "Broker", "field": "id"},
            "cardinality": {
                "of": "Asset",
                "to": "Broker",
                "multiplicity": "many-to-one",
                "optional": False,
            },
        },
    )
    symbol: str = Field(
        json_schema_extra={"type": "string", "nullable": False},
    )
    category: str = Field(
        json_schema_extra={"type": "string", "nullable": False},
    )
    point_size: float = Field(
        default=0.0,
        json_schema_extra={"type": "float", "nullable": False, "default": 0.0},
    )
    digits: int = Field(
        default=0,
        json_schema_extra={"type": "integer", "nullable": False, "default": 0},
    )
    is_active: bool = Field(
        default=True,
        json_schema_extra={"type": "boolean", "nullable": False, "default": True},
    )
    description: str | None = Field(
        default=None,
        json_schema_extra={"type": "string", "nullable": True},
    )
