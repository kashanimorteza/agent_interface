"""The defaults that complete properties an entity leaves unstated.

These complete fields that a definition already declares. They are not a list of
fields to add: a name appearing here alone never introduces a field into an
entity.
"""

from __future__ import annotations

from typing import Any

from .field_spec import FieldType

# Completions matched on the exact field name.
COMMON_FIELD_DEFAULTS: dict[str, dict[str, Any]] = {
    "id": {
        "type": FieldType.INTEGER,
        "nullable": False,
        "auto_increment": True,
        "primary_key": True,
    },
    "name": {
        "type": FieldType.STRING,
        "nullable": False,
        "unique": True,
        "purpose": "The entity's display name.",
    },
    "api_key": {
        "type": FieldType.STRING,
        "nullable": False,
        "credential": True,
        "purpose": "The API key assigned to the entity.",
    },
    "password": {
        "credential": True,
    },
    "status": {
        "type": FieldType.BOOLEAN,
        "nullable": False,
        "default": True,
        "purpose": "Indicates whether the entity is active.",
    },
    "description": {
        "type": FieldType.STRING,
        "nullable": True,
        "purpose": "Describes the entity.",
    },
}

# Completions matched on the shape of the field name, applied after the exact ones.
FIELD_PATTERN_DEFAULTS: list[tuple[str, dict[str, Any]]] = [
    (
        "*_id",
        {
            "type": FieldType.INTEGER,
            "nullable": False,
        },
    ),
]
