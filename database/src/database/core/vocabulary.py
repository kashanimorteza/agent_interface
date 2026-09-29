"""Request and result vocabulary published through Interface."""

from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class DatabaseInstance(StrEnum):
    """The active Instances a request may select."""

    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"


class FilterOperator(StrEnum):
    """Comparison a Filter applies to an Entity Field."""

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


class FilterCombination(StrEnum):
    """How several Filters combine."""

    AND = "AND"
    OR = "OR"


class OrderDirection(StrEnum):
    """Direction of one ordering instruction."""

    ASCENDING = "ascending"
    DESCENDING = "descending"


@dataclass(frozen=True, slots=True)
class Filter:
    """One condition on an Entity Field.

    Attributes:
        field: Name of the Entity Field.
        operator: Comparison to apply.
        value: Value the Field is compared with; ignored by the null operators.
    """

    field: str
    operator: FilterOperator
    value: Any = None

    def __post_init__(self) -> None:
        """Reject a Field name that is not a string or an operator that is not a member."""
        if not isinstance(self.field, str):
            raise TypeError("Filter field must be an Entity Field name string")
        if not isinstance(self.operator, FilterOperator):
            raise TypeError("Filter operator must be a FilterOperator member")


@dataclass(frozen=True, slots=True)
class Order:
    """One ordering instruction on an Entity Field.

    Attributes:
        field: Name of the Entity Field.
        direction: Direction of the ordering.
    """

    field: str
    direction: OrderDirection = OrderDirection.ASCENDING

    def __post_init__(self) -> None:
        """Reject a Field name that is not a string or a direction that is not a member."""
        if not isinstance(self.field, str):
            raise TypeError("Order field must be an Entity Field name string")
        if not isinstance(self.direction, OrderDirection):
            raise TypeError("Order direction must be an OrderDirection member")


@dataclass(frozen=True, slots=True)
class CommandResult:
    """Standard result of Execute Command; a value that does not apply is None.

    Attributes:
        rows: Returned rows, each mapping a column name to a value.
        affected_count: Number of records the command changed.
    """

    rows: list[dict[str, Any]] | None = None
    affected_count: int | None = None
