"""Validated, normalized request forms that Core hands to an Engine unit."""

from dataclasses import dataclass
from typing import Any

from database.core.values import FilterOperator


@dataclass(frozen=True, slots=True)
class Condition:
    """One checked Filter: Field name and Type, operator, and normalized value."""

    field: str
    type: str
    operator: FilterOperator
    value: Any


@dataclass(frozen=True, slots=True)
class Sorting:
    """One checked Order: the Field's name and declared Type and its direction."""

    field: str
    type: str
    descending: bool
