"""Shared behaviour common to every Entity."""

import json
from typing import Self

from sqlmodel import SQLModel


class Foundation(SQLModel):
    """Base of every Entity; supplies JSON conversion and defines no Fields or domain meaning."""

    def to_json(self) -> str:
        """Convert this instance to a JSON string.

        Returns:
            (str): JSON text holding every Field value of the instance.
        """
        return self.model_dump_json()

    @classmethod
    def from_json(cls, data: str | bytes) -> Self:
        """Create an instance from JSON text.

        Args:
            data (str | bytes): JSON text holding Field values.

        Returns:
            (Self): Instance built and validated from the JSON values.
        """
        return cls.model_validate(json.loads(data))
