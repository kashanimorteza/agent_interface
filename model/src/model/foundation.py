"""Provide the conversion behaviour shared by every Entity.

Foundation supplies behaviour only. It adds no Field, constraint, or domain meaning to an Entity.
"""

import json
from typing import Self

from sqlmodel import SQLModel


class Foundation(SQLModel):
    """Base of every Entity, converting it to and from JSON."""

    def to_json(self) -> str:
        """Convert the Entity to its JSON form.

        Returns:
            (str): JSON object holding every declared Field, with decimal and datetime values as strings.
        """
        return self.model_dump_json()

    @classmethod
    def from_json(cls, data: str) -> Self:
        """Construct an Entity from its JSON form.

        Args:
            data (str): JSON object holding the Entity's Fields.

        Returns:
            (Self): Entity whose Field values are restored to their declared Types.
        """
        # Table models skip value conversion in `model_validate_json`, so parse first and validate the mapping.
        return cls.model_validate(json.loads(data))
