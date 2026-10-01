"""The single public entrypoint of Database: its contracts and the gateway every call goes through."""

import dataclasses as _dataclasses
import enum as _enum
import typing as _typing
from collections.abc import Mapping as _Mapping
from collections.abc import Sequence as _Sequence


class FilterOperator(_enum.Enum):
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


class FilterCombination(_enum.Enum):
    """The ways Filters combine."""

    AND = "AND"
    OR = "OR"


class OrderDirection(_enum.Enum):
    """The directions of an Order."""

    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"


class DatabaseError(Exception):
    """The base of every Database failure."""


class ConfigurationError(DatabaseError):
    """The configuration or the selected Instance is invalid."""


class InactiveInstanceError(DatabaseError):
    """An Instance that is not active was selected."""


class InvalidInputError(DatabaseError):
    """The input or a Field reference is invalid."""


class DeclarationMismatchError(DatabaseError):
    """Stored structure or data does not match its Entity Declaration."""


class ConnectionFailureError(DatabaseError):
    """The connection to an Instance could not be made."""


class ExecutionError(DatabaseError):
    """Storage could not execute the request."""


class LifecycleError(DatabaseError):
    """A Lifecycle Command did not complete."""


class DatabaseInstance(_enum.Enum):
    """The active configured Instances; a member carries no connection value."""

    SQLITE = "SQLITE"


@_dataclasses.dataclass(frozen=True)
class Filter:
    """An immutable condition on one Field of an Entity."""

    field: _typing.Any
    operator: FilterOperator
    value: _typing.Any = None

    def __post_init__(self) -> None:
        if isinstance(self.field, str):
            raise InvalidInputError("A Filter takes a Field reference, not a string.")
        if not isinstance(self.operator, FilterOperator):
            raise InvalidInputError("A Filter takes a FilterOperator member.")
        null_test = self.operator in (
            FilterOperator.IS_NULL,
            FilterOperator.IS_NOT_NULL,
        )
        if null_test != (self.value is None):
            raise InvalidInputError(
                f"{self.operator.name} takes no value; every other operator takes one."
            )
        if self.operator is FilterOperator.IN:
            if not isinstance(self.value, (list, tuple, set, frozenset)):
                raise InvalidInputError("IN takes a collection of values.")
            object.__setattr__(self, "value", tuple(self.value))


@_dataclasses.dataclass(frozen=True)
class Order:
    """An immutable ordering on one Field of an Entity."""

    field: _typing.Any
    direction: OrderDirection = OrderDirection.ASCENDING

    def __post_init__(self) -> None:
        if isinstance(self.field, str):
            raise InvalidInputError("An Order takes a Field reference, not a string.")
        if not isinstance(self.direction, OrderDirection):
            raise InvalidInputError("An Order takes an OrderDirection member.")


@_dataclasses.dataclass(frozen=True)
class CommandResult:
    """The outcome of a Database-wide Operation."""

    rows: tuple[_Mapping[str, _typing.Any], ...] | None
    affected: int | None
    columns: tuple[str, ...] | None
    success: bool
    message: str
    instance: DatabaseInstance


@_dataclasses.dataclass(frozen=True)
class LifecycleResult:
    """The outcome of a Lifecycle Command."""

    command: str
    instance: DatabaseInstance
    success: bool
    affected: int | None
    message: str


def _data() -> _typing.Any:
    from database.core import data

    return data


def _tables() -> _typing.Any:
    from database.core import tables

    return tables


def _initial_data() -> _typing.Any:
    from database.core import initial_data

    return initial_data


class Database:
    """The gateway: create one with Database() and call every Operation and Lifecycle Command on it."""

    def add(
        self, entity: _typing.Any, instance: DatabaseInstance | None = None
    ) -> _typing.Any:
        """Store one complete new Entity instance and return the stored Entity, including generated values."""
        return _data().add(entity, instance)

    def update(
        self, entity: _typing.Any, instance: DatabaseInstance | None = None
    ) -> _typing.Any:
        """Replace every mutable Field of the stored record the Entity's id locates; return the stored Entity or None."""
        return _data().update(entity, instance)

    def delete(
        self,
        entity: type[_typing.Any],
        id: _typing.Any,
        instance: DatabaseInstance | None = None,
    ) -> _typing.Any:
        """Delete the record with the id and return it as it was, or None when none exists."""
        return _data().delete_by_id(entity, id, instance)

    def enable(
        self,
        entity: type[_typing.Any],
        id: _typing.Any,
        instance: DatabaseInstance | None = None,
    ) -> _typing.Any:
        """Set only is_active to true and return the final Entity, or None when none exists."""
        return _data().set_active(entity, id, True, instance)

    def disable(
        self,
        entity: type[_typing.Any],
        id: _typing.Any,
        instance: DatabaseInstance | None = None,
    ) -> _typing.Any:
        """Set only is_active to false and return the final Entity, or None when none exists."""
        return _data().set_active(entity, id, False, instance)

    def truncate(
        self, entity: type[_typing.Any], instance: DatabaseInstance | None = None
    ) -> int:
        """Remove every record of the Entity, keep its Table, and return the deleted count."""
        return _data().truncate(entity, instance)

    def list(
        self,
        entity: type[_typing.Any],
        filters: _Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        orders: _Sequence[Order] | None = None,
        limit: int | None = None,
        instance: DatabaseInstance | None = None,
    ) -> _Sequence[_typing.Any]:
        """Return the Entities that match, ordered and limited; a zero or negative limit means no limit."""
        return _data().list_entities(
            entity, filters, combination, orders, limit, instance
        )

    def get_by_id(
        self,
        entity: type[_typing.Any],
        id: _typing.Any,
        instance: DatabaseInstance | None = None,
    ) -> _typing.Any:
        """Return the Entity with the id, or None when none exists."""
        return _data().get_by_id(entity, id, instance)

    def count(
        self,
        entity: type[_typing.Any],
        filters: _Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> int:
        """Return how many Entities match."""
        return _data().count(entity, filters, combination, instance)

    def sum(
        self,
        entity: type[_typing.Any],
        field: _typing.Any,
        filters: _Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> _typing.Any:
        """Return the total of a numeric Field, ignoring nulls; zero when nothing matches."""
        return _data().aggregate("sum", entity, field, filters, combination, instance)

    def min(
        self,
        entity: type[_typing.Any],
        field: _typing.Any,
        filters: _Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> _typing.Any:
        """Return the smallest value of a comparable Field, ignoring nulls; None when nothing matches."""
        return _data().aggregate("min", entity, field, filters, combination, instance)

    def max(
        self,
        entity: type[_typing.Any],
        field: _typing.Any,
        filters: _Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> _typing.Any:
        """Return the largest value of a comparable Field, ignoring nulls; None when nothing matches."""
        return _data().aggregate("max", entity, field, filters, combination, instance)

    def execute_command(
        self,
        command: str,
        parameters: _Mapping[str, _typing.Any] | _Sequence[_typing.Any] | None = None,
        instance: DatabaseInstance | None = None,
    ) -> CommandResult:
        """Run a native command in the Instance Engine's query language with bound parameters."""
        return _data().execute_command(command, parameters, instance)

    def create_tables(
        self, instance: DatabaseInstance | None = None
    ) -> LifecycleResult:
        """Create every Table from the Model Entities; stop on a difference with an existing Table."""
        return _tables().create_tables(instance)

    def insert_initial_data(
        self, instance: DatabaseInstance | None = None
    ) -> LifecycleResult:
        """Insert every missing Initial Data record, skipping identical records and failing on a conflict."""
        return _initial_data().insert_initial_data(instance)

    def prepare(self, instance: DatabaseInstance | None = None) -> LifecycleResult:
        """Run create_tables and then insert_initial_data, stopping when create_tables fails."""
        return _initial_data().prepare(instance)
