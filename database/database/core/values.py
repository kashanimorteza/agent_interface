"""Values (Core): immutable forms, enumerations, and Results."""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from database.core.errors import InvalidInputError


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


@dataclass(frozen=True)
class Filter:
    field: Any
    operator: FilterOperator
    value: Any = None

    def __post_init__(self) -> None:
        if isinstance(self.field, str):
            raise InvalidInputError("A Filter needs a Field reference, not a string")
        if not isinstance(self.operator, FilterOperator):
            raise InvalidInputError("A Filter needs a FilterOperator member")


@dataclass(frozen=True)
class Order:
    field: Any
    direction: OrderDirection = OrderDirection.ASCENDING

    def __post_init__(self) -> None:
        if isinstance(self.field, str):
            raise InvalidInputError("An Order needs a Field reference, not a string")
        if not isinstance(self.direction, OrderDirection):
            raise InvalidInputError("An Order needs an OrderDirection member")


@dataclass(frozen=True)
class CheckedFilter:
    field: str
    type: str
    operator: FilterOperator
    value: Any


@dataclass(frozen=True)
class CheckedOrder:
    field: str
    type: str
    descending: bool


@dataclass(frozen=True)
class CommandResult:
    rows: tuple[dict[str, Any], ...] | None
    affected: int | None
    columns: tuple[str, ...] | None
    success: bool
    message: str
    instance: Enum


@dataclass(frozen=True)
class SetupResult:
    command: str
    instance: Enum
    success: bool
    affected: int | None
    message: str


@dataclass(frozen=True)
class Connection:
    """The resolved connection Core hands to an Engine unit; never published."""

    instance: str
    engine: str
    host: str | None
    port: int | None
    database: str
    username: str | None = field(repr=False)
    password: str | None = field(repr=False)
    options: dict[str, Any] = field(repr=False)
    parameters: dict[str, Any] = field(repr=False)
    storage_path: Path | None = None
