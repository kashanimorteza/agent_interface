"""The immutable forms and enumerations that Core and the published groups share."""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
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


@dataclass(frozen=True, slots=True)
class Filter:
    """A condition a consumer builds: a Field reference, an operator and a value."""

    field: Any
    operator: FilterOperator
    value: Any = None


@dataclass(frozen=True, slots=True)
class Order:
    """An ordering a consumer builds: a Field reference and a direction."""

    field: Any
    direction: OrderDirection = OrderDirection.ASCENDING


@dataclass(frozen=True, slots=True)
class CheckedFilter:
    """A Filter checked against its Entity: Field name, declared Type, operator and normalized value."""

    field: str
    type: str
    operator: FilterOperator
    value: Any


@dataclass(frozen=True, slots=True)
class CheckedOrder:
    """An Order checked against its Entity: Field name, declared Type and whether it descends."""

    field: str
    type: str
    descending: bool


@dataclass(frozen=True, slots=True)
class CommandResult:
    """The outcome of a Command Operation."""

    rows: tuple[dict[str, Any], ...] | None
    affected: int | None
    columns: tuple[str, ...] | None
    success: bool
    message: str
    instance: Enum


@dataclass(frozen=True, slots=True)
class SetupResult:
    """The outcome of a Setup Operation."""

    command: str
    instance: Enum
    success: bool
    affected: int | None
    message: str


@dataclass(frozen=True, slots=True)
class Connection:
    """What Core hands an Engine unit: the resolved connection of one Instance. It is never published."""

    engine: str = field(repr=False)
    parameters: dict[str, Any] = field(repr=False)
    host: str | None = field(repr=False)
    port: int | None = field(repr=False)
    database: str = field(repr=False)
    username: str | None = field(repr=False)
    password: str | None = field(repr=False)
    options: dict[str, Any] = field(repr=False)
    location: Path | None = field(repr=False)
