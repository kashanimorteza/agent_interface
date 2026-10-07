from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from typing import Any


class FilterOperator(Enum):
    EQUALS = "EQUALS"
    NOT_EQUALS = "NOT_EQUALS"
    GREATER_THAN = "GREATER_THAN"
    GREATER_OR_EQUAL = "GREATER_OR_EQUAL"
    LESS_THAN = "LESS_THAN"
    LESS_OR_EQUAL = "LESS_OR_EQUAL"
    IN = "IN"
    CONTAINS = "CONTAINS"
    STARTS_WITH = "STARTS_WITH"
    ENDS_WITH = "ENDS_WITH"
    IS_NULL = "IS_NULL"
    IS_NOT_NULL = "IS_NOT_NULL"


class FilterCombination(Enum):
    AND = "AND"
    OR = "OR"


class OrderDirection(Enum):
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"


class DatabaseInstance(Enum):
    SQLITE = "SQLITE"


@dataclass(frozen=True)
class Filter:
    field: Any
    operator: FilterOperator
    value: Any = None

    def __post_init__(self) -> None:
        if isinstance(self.value, list | set | frozenset):
            object.__setattr__(self, "value", tuple(self.value))


@dataclass(frozen=True)
class Order:
    field: Any
    direction: OrderDirection = OrderDirection.ASCENDING


@dataclass(frozen=True)
class CommandResult:
    rows: tuple[Mapping[str, Any], ...] | None
    affected: int | None
    columns: tuple[str, ...] | None
    success: bool
    message: str
    instance: DatabaseInstance


@dataclass(frozen=True)
class SetupResult:
    command: str
    instance: DatabaseInstance
    success: bool
    affected: int | None
    message: str
