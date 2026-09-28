"""Foundation layer: shared conversion capabilities of every Entity."""

import json
from typing import Self

from sqlmodel import SQLModel


class Foundation(SQLModel):
    """Base of every Entity; converts an Entity to JSON and constructs one from JSON."""

    def to_json(self) -> str:
        """Convert the Entity to JSON.

        Returns:
            (str): JSON holding exactly the Entity's Field values, in declared Field order.
        """
        data = self.model_dump(mode="json")
        return json.dumps(
            {name: data[name] for name in type(self).model_fields},
            separators=(",", ":"),
            ensure_ascii=False,
        )

    @classmethod
    def from_json(cls, data: str) -> Self:
        """Construct an Entity from JSON.

        Args:
            data (str): JSON holding Field values.

        Returns:
            (Self): The constructed Entity.
        """
        return cls.model_validate(json.loads(data))
