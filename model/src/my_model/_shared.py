from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class Relationship:
    target: str
    cardinality: Literal["one", "many"]
    field: str | None = None
    optional: bool = False
