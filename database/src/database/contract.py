"""Request and result types shared by Interface, Data, and Engine."""

from dataclasses import dataclass
from enum import StrEnum
from typing import Any


@dataclass(frozen=True, slots=True)
class CommandResult:
    """Standard result of Execute Command.

    Attributes:
        rows (list[dict[str, Any]] | None): Rows returned by the command, each a mapping from column name to value, or None when the command returns none.
        affected_count (int | None): Number of records the command affected, or None when it does not apply.
    """

    rows: list[dict[str, Any]] | None
    affected_count: int | None


class Direction(StrEnum):
    """Direction of an Order."""

    ASCENDING = "ascending"
    DESCENDING = "descending"


@dataclass(slots=True)
class Order:
    """One ordering instruction.

    Attributes:
        field (Any): A Field selected from the Entity class to order by.
        direction (Direction): Ascending or descending.
    """

    field: Any
    direction: Direction = Direction.ASCENDING

    def __post_init__(self) -> None:
        if not isinstance(self.direction, Direction):
            raise TypeError("Order direction must be a Direction enum member")


class Combination(StrEnum):
    """How several Filters combine."""

    AND = "AND"
    OR = "OR"


class Operator(StrEnum):
    """Comparison a Filter applies."""

    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    GREATER_THAN = "greater_than"
    GREATER_OR_EQUAL = "greater_or_equal"
    LESS_THAN = "less_than"
    LESS_OR_EQUAL = "less_or_equal"
    IN = "in"
    CONTAINS = "contains"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"
    IS_NULL = "is_null"
    IS_NOT_NULL = "is_not_null"


@dataclass(slots=True)
class Filter:
    """One condition a record must satisfy.

    Attributes:
        field (Any): A Field selected from the Entity class to test.
        operator (Operator): Comparison to apply.
        value (Any): Value to compare with; unused by `is_null` and `is_not_null`, a sequence for `in`.
    """

    field: Any
    operator: Operator
    value: Any = None

    def __post_init__(self) -> None:
        if not isinstance(self.operator, Operator):
            raise TypeError("Filter operator must be an Operator enum member")
