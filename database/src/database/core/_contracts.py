"""Public contracts: Instance members, query vocabulary, query values, and results."""

from collections.abc import Collection, Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, cast

from database.core._failures import InvalidInputFailure


class DatabaseInstance(StrEnum):
    """One member for every active configured Instance; it carries no credential."""

    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"


class FilterOperator(StrEnum):
    """The condition a Filter applies to a Field."""

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


class FilterCombination(StrEnum):
    """How several Filters combine."""

    AND = "AND"
    OR = "OR"


class OrderDirection(StrEnum):
    """The direction an Order sorts in."""

    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"


class _Absent:
    """Marks a Filter value that was not supplied."""

    __slots__ = ()

    def __repr__(self) -> str:
        return "ABSENT"

    def __bool__(self) -> bool:
        return False


ABSENT = _Absent()

NULL_TESTING = frozenset({FilterOperator.IS_NULL, FilterOperator.IS_NOT_NULL})
TEXTUAL = frozenset(
    {FilterOperator.CONTAINS, FilterOperator.STARTS_WITH, FilterOperator.ENDS_WITH}
)


@dataclass(frozen=True, slots=True)
class Filter:
    """An immutable condition: a Field, an operator, and a value when one is needed.

    IS_NULL and IS_NOT_NULL take no value; IN takes a collection.
    """

    field: str
    operator: FilterOperator
    value: Any = ABSENT

    def __post_init__(self) -> None:
        if not isinstance(self.field, str) or not self.field:  # pyright: ignore[reportUnnecessaryIsInstance]
            raise InvalidInputFailure("A Filter names a Field.")
        if not isinstance(self.operator, FilterOperator):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise InvalidInputFailure("A Filter operator is a FilterOperator member.")
        if self.operator in NULL_TESTING:
            if self.value is not ABSENT:
                raise InvalidInputFailure(f"{self.operator.name} takes no value.")
            return
        if self.value is ABSENT:
            raise InvalidInputFailure(f"{self.operator.name} needs a value.")
        if self.operator is FilterOperator.IN:
            raw: object = self.value
            if isinstance(raw, (str, bytes, Mapping)) or not isinstance(
                raw, Collection
            ):
                raise InvalidInputFailure("IN takes a collection of values.")
            object.__setattr__(self, "value", tuple(cast(Collection[Any], raw)))


@dataclass(frozen=True, slots=True)
class Order:
    """An immutable ordering instruction: a Field and a direction."""

    field: str
    direction: OrderDirection = OrderDirection.ASCENDING

    def __post_init__(self) -> None:
        if not isinstance(self.field, str) or not self.field:  # pyright: ignore[reportUnnecessaryIsInstance]
            raise InvalidInputFailure("An Order names a Field.")
        if not isinstance(self.direction, OrderDirection):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise InvalidInputFailure("An Order direction is an OrderDirection member.")


@dataclass(frozen=True, slots=True)
class CommandResult:
    """The public result of ExecuteCommand."""

    rows: list[dict[str, Any]] | None
    affected: int | None
    columns: list[str] | None
    success: bool
    message: str
    instance: DatabaseInstance


@dataclass(frozen=True, slots=True)
class LifecycleResult:
    """The public result of a Lifecycle Command."""

    command: str
    instance: DatabaseInstance
    success: bool
    affected: int | None
    message: str


@dataclass(frozen=True, slots=True)
class Query:
    """A fully resolved query: every default applied, ready for an Instance."""

    filters: tuple[Filter, ...]
    combination: FilterCombination
    orders: tuple[Order, ...]
    limit: int
