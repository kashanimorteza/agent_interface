"""The immutable forms, enumerations, and Results of the Database contract."""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class FilterOperator(Enum):
    """How a Filter compares a Field with its value."""

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
    """How several Filters combine."""

    AND = "AND"
    OR = "OR"


class OrderDirection(Enum):
    """The direction of an Order."""

    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"


class database_instance(Enum):
    """The active Instances a call can run on."""

    SQLITE = "sqlite"


@dataclass(frozen=True, slots=True)
class Filter:
    """One condition on a Field of the given Entity."""

    field: Any
    operator: FilterOperator
    value: Any = None


@dataclass(frozen=True, slots=True)
class Order:
    """One ordering on a Field of the given Entity."""

    field: Any
    direction: OrderDirection = OrderDirection.ASCENDING


@dataclass(frozen=True, slots=True)
class CheckedFilter:
    """A Filter checked against its Entity: the Field's name and declared Type."""

    field: str
    type: str
    operator: FilterOperator
    value: Any


@dataclass(frozen=True, slots=True)
class CheckedOrder:
    """An Order checked against its Entity: the Field's name and declared Type."""

    field: str
    type: str
    descending: bool


@dataclass(frozen=True, slots=True)
class CommandResult:
    """The outcome of a native command."""

    rows: list[dict[str, Any]] | None
    affected: int | None
    columns: list[str] | None
    success: bool
    message: str
    instance: database_instance


@dataclass(frozen=True, slots=True)
class SetupResult:
    """The outcome of a Setup Operation."""

    command: str
    instance: database_instance
    success: bool
    affected: int | None
    message: str
