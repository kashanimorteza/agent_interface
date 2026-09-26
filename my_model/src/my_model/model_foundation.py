"""Shared behaviour of Model Entities.

Foundation converts an instance to JSON and creates an instance from JSON. It defines no Fields,
constraints, or domain meaning.
"""

import json
from typing import Self

from sqlmodel import SQLModel


class ModelFoundation(SQLModel):
    """Base of every Entity, providing JSON conversion."""

    @classmethod
    def from_json(cls, data: str) -> Self:
        """Create an instance from JSON.

        Args:
            data (str): JSON text holding the Field values.

        Returns:
            (Self): Instance restored from the JSON.
        """
        return cls.model_validate(json.loads(data))

    def to_json(self) -> str:
        """Convert the instance to JSON.

        Returns:
            (str): JSON text holding every Field value.
        """
        return self.model_dump_json()
