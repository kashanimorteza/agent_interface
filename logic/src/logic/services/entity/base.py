"""The shared foundation every Entity's Service is built on; internal to the Entity Service."""

from collections.abc import Mapping, Sequence
from typing import Any, ClassVar, Protocol

from database.interface import Database, Filter, FilterCombination, Order

from logic.core.credentials import WITHHELD, CredentialProtector, Treatment
from logic.core.dependency import Dependency
from logic.core.outcome import Outcome, OutcomeKind


class Published(Protocol):
    """What every Entity Model publishes that Logic relies on."""

    declaration: ClassVar[Any]

    def model_dump(self) -> dict[str, Any]:
        """Return the Field values."""
        ...


class EntityServiceBase[T: Published]:
    """Shared Entity-bound Actions; an Entity's Service names its Entity and inherits them."""

    entity: type[T]
    credentials: ClassVar[Mapping[str, Treatment]] = {}

    def __init__(
        self,
        database: Database,
        dependency: Dependency,
        protector: CredentialProtector,
    ) -> None:
        """Bind the Service to the Database it reaches and the bounds it works within.

        Args:
            database (Database): Database's published surface.
            dependency (Dependency): Bounded use of the dependency.
            protector (CredentialProtector): Protection of credential Fields before storage.
        """
        self._database = database
        self._dependency = dependency
        self._protector = protector

    @property
    def _name(self) -> str:
        return self.entity.declaration.name

    def _checked(self, entity: Any) -> Outcome[T]:
        if not isinstance(entity, self.entity):
            return Outcome.failure(OutcomeKind.INVALID, f"a {self._name} is required")
        try:
            build: Any = self.entity
            return Outcome.success(build(**entity.model_dump()))
        except ValueError as error:
            return Outcome.failure(OutcomeKind.INVALID, str(error))

    def _protected(self, entity: Any, skip: Sequence[str] = ()) -> Any:
        for name, treatment in self.credentials.items():
            value = getattr(entity, name)
            if value is not None and name not in skip:
                setattr(entity, name, self._protector.protect(treatment, value))
        return entity

    def _unchanged(self, entity: Any) -> list[str]:
        return [n for n in self.credentials if getattr(entity, n) == WITHHELD]

    def _restored(self, entity: Any, unchanged: Sequence[str]) -> Outcome[Any]:
        if unchanged:
            existing = self._present(
                self._dependency.call(
                    lambda: self._database.get_by_id(self.entity, entity.id),
                    repeatable=True,
                )
            )
            if not existing.succeeded:
                return existing
            for name in unchanged:
                setattr(entity, name, getattr(existing.value, name))
        return Outcome.success(self._protected(entity, unchanged))

    def _masked(self, entity: Any) -> Any:
        build: Any = self.entity
        shown = build(**entity.model_dump())
        for name in self.credentials:
            if getattr(shown, name) is not None:
                setattr(shown, name, WITHHELD)
        return shown

    def _shown(self, outcome: Outcome[Any]) -> Outcome[Any]:
        if not self.credentials or not outcome.succeeded:
            return outcome
        if isinstance(outcome.value, self.entity):
            return Outcome.success(self._masked(outcome.value))
        return Outcome.success([self._masked(e) for e in outcome.value or []])

    def _selectable(self, *fields: str) -> Outcome[Any] | None:
        if any(name in self.credentials for name in fields):
            return Outcome.failure(
                OutcomeKind.INVALID,
                "a credential Field cannot be used to select, order, or total records",
            )
        return None

    def _absent(self) -> Outcome[Any]:
        return Outcome.failure(OutcomeKind.NOT_FOUND, f"no {self._name} has that id")

    def _present(self, outcome: Outcome[Any]) -> Outcome[Any]:
        return (
            self._absent() if outcome.succeeded and outcome.value is None else outcome
        )

    def add(self, entity: T) -> Outcome[T]:
        """Persist a new record.

        Args:
            entity (T): Complete Entity instance; its values must satisfy the constraints Model declares.

        Returns:
            (Outcome): The created Entity with any generated values, or an invalid, conflict, broken-reference, or unavailable failure; nothing is stored on failure.
        """
        checked = self._checked(entity)
        if not checked.succeeded:
            return checked
        if self._unchanged(checked.value):
            return Outcome.failure(
                OutcomeKind.INVALID, "a new record needs its credentials supplied"
            )
        stored = self._protected(checked.value)
        return self._shown(self._dependency.call(lambda: self._database.add(stored)))

    def get_by_id(self, record_id: int) -> Outcome[T]:
        """Retrieve one record.

        Args:
            record_id (int): Id of the record.

        Returns:
            (Outcome): The Entity, or a not-found, invalid, or unavailable failure.
        """
        return self._shown(
            self._present(
                self._dependency.call(
                    lambda: self._database.get_by_id(self.entity, record_id),
                    repeatable=True,
                )
            )
        )

    def update(self, entity: T) -> Outcome[T]:
        """Replace every mutable Field of an existing record, located by its id.

        Args:
            entity (T): Complete Entity instance holding the id of the record.

        Returns:
            (Outcome): The updated Entity, or a not-found, invalid, conflict, broken-reference, or unavailable failure; the record is unchanged on failure.
        """
        checked = self._checked(entity)
        if not checked.succeeded:
            return checked
        restored = self._restored(checked.value, self._unchanged(checked.value))
        if not restored.succeeded:
            return restored
        return self._shown(
            self._present(
                self._dependency.call(
                    lambda: self._database.update(restored.value), repeatable=True
                )
            )
        )

    def delete(self, record_id: int) -> Outcome[bool]:
        """Remove one record.

        Args:
            record_id (int): Id of the record.

        Returns:
            (Outcome): True once removed, or a not-found, invalid, broken-reference (still referred to), or unavailable failure.
        """
        outcome = self._dependency.call(
            lambda: self._database.delete(self.entity, record_id)
        )
        return self._absent() if outcome.succeeded and not outcome.value else outcome

    def enable(self, record_id: int) -> Outcome[T]:
        """Mark one record active.

        Args:
            record_id (int): Id of the record.

        Returns:
            (Outcome): The Entity, or a not-found, invalid, or unavailable failure.
        """
        return self._shown(
            self._present(
                self._dependency.call(
                    lambda: self._database.enable(self.entity, record_id),
                    repeatable=True,
                )
            )
        )

    def disable(self, record_id: int) -> Outcome[T]:
        """Mark one record inactive.

        Args:
            record_id (int): Id of the record.

        Returns:
            (Outcome): The Entity, or a not-found, invalid, or unavailable failure.
        """
        return self._shown(
            self._present(
                self._dependency.call(
                    lambda: self._database.disable(self.entity, record_id),
                    repeatable=True,
                )
            )
        )

    def list(
        self,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        orders: Sequence[Order] | None = None,
        limit: int | None = None,
    ) -> Outcome[Sequence[T]]:
        """Retrieve the matching records.

        Args:
            filters (Sequence, optional): Conditions on Entity Fields.
            combination (FilterCombination, optional): How the filters combine.
            orders (Sequence, optional): Ordering instructions, applied in the order given.
            limit (int, optional): Most records to return; zero or less means no limit.

        Returns:
            (Outcome): The matching Entities (an empty result is a success), or an invalid or unavailable failure.
        """
        refused = self._selectable(
            *(f.field for f in filters or ()), *(o.field for o in orders or ())
        )
        if refused:
            return refused
        return self._shown(
            self._dependency.call(
                lambda: [
                    *self._database.list(
                        self.entity, filters, combination, orders, limit
                    )
                ],
                repeatable=True,
            )
        )

    def count(
        self,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
    ) -> Outcome[int]:
        """Count the matching records.

        Args:
            filters (Sequence, optional): Conditions on Entity Fields.
            combination (FilterCombination, optional): How the filters combine.

        Returns:
            (Outcome): The number of matching records (zero when none match), or an invalid or unavailable failure.
        """
        refused = self._selectable(*(f.field for f in filters or ()))
        if refused:
            return refused
        return self._dependency.call(
            lambda: self._database.count(self.entity, filters, combination),
            repeatable=True,
        )

    def sum(
        self,
        field: str,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
    ) -> Outcome[Any]:
        """Total one numeric Field over the matching records, ignoring absent values.

        Args:
            field (str): Name of the Field.
            filters (Sequence, optional): Conditions on Entity Fields.
            combination (FilterCombination, optional): How the filters combine.

        Returns:
            (Outcome): The total (zero when no usable value exists), or an invalid failure for an unknown or non-numeric Field, or an unavailable failure.
        """
        refused = self._selectable(field, *(f.field for f in filters or ()))
        if refused:
            return refused
        return self._dependency.call(
            lambda: self._database.sum(self.entity, field, filters, combination),
            repeatable=True,
        )

    def min(
        self,
        field: str,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
    ) -> Outcome[Any]:
        """Find the smallest value of one Field over the matching records, ignoring absent values.

        Args:
            field (str): Name of the Field.
            filters (Sequence, optional): Conditions on Entity Fields.
            combination (FilterCombination, optional): How the filters combine.

        Returns:
            (Outcome): The smallest value (a success holding no value when none is usable), or an invalid failure for an unknown Field, or an unavailable failure.
        """
        refused = self._selectable(field, *(f.field for f in filters or ()))
        if refused:
            return refused
        return self._dependency.call(
            lambda: self._database.min(self.entity, field, filters, combination),
            repeatable=True,
        )

    def max(
        self,
        field: str,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
    ) -> Outcome[Any]:
        """Find the largest value of one Field over the matching records, ignoring absent values.

        Args:
            field (str): Name of the Field.
            filters (Sequence, optional): Conditions on Entity Fields.
            combination (FilterCombination, optional): How the filters combine.

        Returns:
            (Outcome): The largest value (a success holding no value when none is usable), or an invalid failure for an unknown Field, or an unavailable failure.
        """
        refused = self._selectable(field, *(f.field for f in filters or ()))
        if refused:
            return refused
        return self._dependency.call(
            lambda: self._database.max(self.entity, field, filters, combination),
            repeatable=True,
        )

    def truncate(self) -> Outcome[int]:
        """Remove every record of the Entity.

        Returns:
            (Outcome): The number of removed records, or a broken-reference (still referred to) or unavailable failure; nothing is removed on failure.
        """
        return self._dependency.call(lambda: self._database.truncate(self.entity))
