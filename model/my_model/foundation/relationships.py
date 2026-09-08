"""How entities are connected, stated once with the entities themselves.

A relationship says what is connected, how many of each side participate, which
side is optional, and which field carries the connection. How that connection is
physically realized is decided by whichever layer stores it.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Cardinality(str, Enum):
    """How many of each side participate in a connection."""

    ONE_TO_ONE = "one_to_one"
    MANY_TO_ONE = "many_to_one"
    ONE_TO_MANY = "one_to_many"
    MANY_TO_MANY = "many_to_many"


@dataclass(frozen=True, slots=True)
class Relationship:
    """One conceptual connection from this entity to another."""

    target: str
    cardinality: Cardinality
    role: str
    field: str | None = None
    optional: bool = False

    def __str__(self) -> str:
        through = f" through {self.field}" if self.field else ""
        return f"{self.cardinality.value} {self.target} as {self.role}{through}"
