"""The public vocabulary, values, and results a consumer imports and passes in place of strings."""

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Any

from sqlalchemy.orm.attributes import InstrumentedAttribute

from database.core.errors import InvalidInputError


class FilterOperator(Enum):
    """The comparison operators of a Filter."""

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
    """The ways Filters combine."""

    AND = "AND"
    OR = "OR"


class OrderDirection(Enum):
    """The directions of an Order."""

    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"


class DatabaseInstance(Enum):
    """The active configured Instances; a member carries no connection value."""

    SQLITE = "SQLITE"


@dataclass(frozen=True, slots=True)
class Filter:
    """An immutable condition: a Field reference of an Entity, an operator, and a value.

    The value is absent for the null tests and a collection for IN.
    """

    field: Any
    operator: FilterOperator
    value: Any = None

    def __post_init__(self) -> None:
        if not isinstance(self.field, InstrumentedAttribute):
            raise InvalidInputError("A Filter needs a Field reference of an Entity, not a name")
        if not isinstance(self.operator, FilterOperator):
            raise InvalidInputError("A Filter needs a FilterOperator member")
        if self.operator in (FilterOperator.IS_NULL, FilterOperator.IS_NOT_NULL):
            if self.value is not None:
                raise InvalidInputError("A null test takes no value")
        elif self.operator is FilterOperator.IN:
            if isinstance(self.value, str | bytes) or not isinstance(
                self.value, list | tuple | set | frozenset
            ):
                raise InvalidInputError("IN needs a collection of values")
            object.__setattr__(self, "value", tuple(self.value))
        elif self.value is None:
            raise InvalidInputError(f"{self.operator.name} needs a value")


@dataclass(frozen=True, slots=True)
class Order:
    """An immutable ordering: a Field reference of an Entity and a direction."""

    field: Any
    direction: OrderDirection = OrderDirection.ASCENDING

    def __post_init__(self) -> None:
        if not isinstance(self.field, InstrumentedAttribute):
            raise InvalidInputError("An Order needs a Field reference of an Entity, not a name")
        if not isinstance(self.direction, OrderDirection):
            raise InvalidInputError("An Order needs an OrderDirection member")


@dataclass(frozen=True, slots=True)
class CommandResult:
    """The outcome of a Database-wide Operation."""

    rows: tuple[Mapping[str, Any], ...] | None
    affected: int | None
    columns: tuple[str, ...] | None
    success: bool
    message: str
    instance: DatabaseInstance

    def __post_init__(self) -> None:
        if self.rows is not None:
            frozen = tuple(MappingProxyType(dict(row)) for row in self.rows)
            object.__setattr__(self, "rows", frozen)
        if self.columns is not None:
            object.__setattr__(self, "columns", tuple(self.columns))


@dataclass(frozen=True, slots=True)
class LifecycleResult:
    """The outcome of a Lifecycle Command."""

    command: str
    instance: DatabaseInstance
    success: bool
    affected: int | None
    message: str
