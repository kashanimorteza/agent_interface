"""Shared conversion behaviour for every Entity."""

import json
from typing import Any, Self

from sqlmodel import SQLModel


class Model_Foundation(SQLModel):
    """Converts an Entity instance to JSON and back. Defines no Fields."""

    def to_json(self) -> str:
        """Return this instance as a JSON string."""
        return self.model_dump_json()

    @classmethod
    def from_json(cls, data: str | bytes) -> Self:
        """Create an instance from a JSON string."""
        values: dict[str, Any] = json.loads(data)
        return cls.model_validate(values)
