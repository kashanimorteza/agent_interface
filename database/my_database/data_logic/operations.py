"""One pipeline that serves every definition.

Nothing here is written per definition. An operation is given a definition — the
type itself, or an instance of it — works out what it needs from that
definition's own resolved fields, connections and rules, and runs. A new
definition costs no new code here.

What comes back is the definition's own partial view with its credential fields
left out: an output that excludes credentials is still that definition, and the
stored form of a credential never leaves this layer.
"""

from __future__ import annotations

from typing import Any, Iterable, Mapping

from my_model import Entity, PartialView, is_stated
from sqlalchemy import Connection, delete as sql_delete, insert, select, update as sql_update
from sqlalchemy.sql import Select

from ..contract import OperationError
from . import credentials, mapping


ENABLE = "enable"
DISABLE = "disable"
STATUS_FIELD = "status"
_ACTIONS = {ENABLE: True, DISABLE: False}


# <!-------------------------------------------- what a caller may pass -->


def resolve_definition(subject: Any) -> tuple[type[Entity], dict[str, Any] | None]:
    """The definition a caller is working with, and any values it carried.

    A definition is passed as the type or as an instance of it. A bare name with
    a loose set of values is not a definition and is refused.
    """

    if isinstance(subject, str):
        raise OperationError(
            "a definition is passed as the definition itself, not as its name; "
            f"received the string {subject!r}"
        )
    if isinstance(subject, type) and issubclass(subject, Entity):
        return subject, None
    if isinstance(subject, Entity):
        return type(subject), subject.model_dump()
    raise OperationError(f"{subject!r} is not a published definition")


def _check_fields(entity: type[Entity], names: Iterable[str], what: str) -> None:
    unknown = [name for name in names if name not in entity.entity_fields]
    if unknown:
        raise OperationError(f"{entity.entity_name} has no field {unknown} to {what} by")


def _protect(entity: type[Entity], values: Mapping[str, Any]) -> dict[str, Any]:
    """Values on their way in, with each credential given its treatment."""

    resolved = credentials.treatments(entity)
    protected: dict[str, Any] = {}
    for name, value in values.items():
        treatment = resolved.get(name)
        protected[name] = credentials.protect(value, treatment) if treatment else value
    return protected


def _present(entity: type[Entity], row: Mapping[str, Any]) -> PartialView:
    """A stored row as the definition's own view, without its credentials."""

    hidden = set(credentials.treatments(entity))
    return entity.Partial.model_validate(
        {name: value for name, value in row.items() if name not in hidden}
    )


def validate_stored(entity: type[Entity], row: Mapping[str, Any]) -> None:
    """Check a stored row against the definition's own validation.

    The definitions already judge what their values can settle, so this reuses
    them rather than keeping a second copy of the same rules here.
    """

    # A credential's stored form is still a value of the kind the field
    # declares, and what the supplied value had to satisfy was checked before it
    # was ever transformed.
    entity(**dict(row))


# <!-------------------------------------------- the operations -->


class Operations:
    """The definition-driven pipeline, run against one open connection."""

    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    # <!---------------------------- create -->

    def create(self, subject: Any, values: Mapping[str, Any] | None = None) -> PartialView:
        entity, carried = resolve_definition(subject)
        supplied = dict(carried if carried is not None else (values or {}))
        if carried is not None and values:
            supplied.update(values)

        key = mapping.identifying_field(entity)
        if supplied.get(key) is None:
            supplied.pop(key, None)
        _check_fields(entity, supplied, "create")

        # The definition judges its own values before anything is stored, and
        # resolves its own declared defaults while it is at it.
        checked = entity(**supplied).model_dump()
        checked.pop(key, None)

        table = mapping.table_for(entity)
        result = self._connection.execute(insert(table).values(**_protect(entity, checked)))
        identifier = result.inserted_primary_key[0]
        stored = self.read(entity, {key: identifier})
        if stored is None:  # pragma: no cover - the row was just written
            raise OperationError(f"{entity.entity_name} was stored but cannot be read back")
        return stored

    # <!---------------------------- read and list -->

    def read(self, subject: Any, criteria: Mapping[str, Any]) -> PartialView | None:
        found = self.list(subject, criteria, limit=1)
        return found[0] if found else None

    def list(
        self,
        subject: Any,
        criteria: Mapping[str, Any] | None = None,
        *,
        limit: int | None = None,
        offset: int | None = None,
        order_by: str | None = None,
    ) -> list[PartialView]:
        entity, _ = resolve_definition(subject)
        table = mapping.table_for(entity)
        statement: Select = select(table)
        statement = _where(statement, entity, table, criteria)

        if order_by is not None:
            _check_fields(entity, [order_by], "order")
            statement = statement.order_by(table.c[order_by])
        if offset is not None:
            statement = statement.offset(offset)
        if limit is not None:
            statement = statement.limit(limit)

        rows = self._connection.execute(statement).mappings().all()
        return [_present(entity, row) for row in rows]

    # <!---------------------------- update and delete -->

    def update(self, subject: Any, criteria: Mapping[str, Any], changes: Any) -> int:
        entity, _ = resolve_definition(subject)
        stated = _stated_changes(entity, changes)
        if not stated:
            return 0

        table = mapping.table_for(entity)
        statement = _where(sql_update(table), entity, table, criteria)
        affected = self._connection.execute(
            statement.values(**_protect(entity, stated))
        ).rowcount

        # What the change produced is judged by the definition before it stands.
        for row in self._connection.execute(
            _where(select(table), entity, table, criteria)
        ).mappings():
            validate_stored(entity, row)
        return affected

    def delete(self, subject: Any, criteria: Mapping[str, Any]) -> int:
        entity, _ = resolve_definition(subject)
        table = mapping.table_for(entity)
        statement = _where(sql_delete(table), entity, table, criteria)
        return self._connection.execute(statement).rowcount

    # <!---------------------------- status -->

    def set_status(self, subject: Any, criteria: Mapping[str, Any], action: str) -> int:
        entity, _ = resolve_definition(subject)
        if STATUS_FIELD not in entity.entity_fields:
            raise OperationError(
                f"{entity.entity_name} declares no {STATUS_FIELD} field, so it cannot be "
                f"enabled or disabled"
            )
        if action not in _ACTIONS:
            raise OperationError(
                f"{action!r} is not an action; enabling and disabling are the only two"
            )
        return self.update(entity, criteria, {STATUS_FIELD: _ACTIONS[action]})

    # <!---------------------------- controlled commands -->

    def execute(
        self,
        statement: str,
        parameters: Mapping[str, Any] | None = None,
        *,
        engine: str,
        engine_specific: str | None = None,
    ):
        """Run a controlled command on this same unit of work."""

        from .commands import run

        return run(
            self._connection,
            statement,
            parameters,
            engine=engine,
            engine_specific=engine_specific,
        )

    # <!---------------------------- declared starting records -->

    def seed(self):
        """Store the declared starting records through this same pipeline."""

        from .seeding import seed

        return seed(self)

    # <!---------------------------- credentials -->

    def credential_matches(
        self, subject: Any, criteria: Mapping[str, Any], field: str, candidate: str
    ) -> bool:
        """Whether a supplied value is the one behind a stored credential."""

        entity, _ = resolve_definition(subject)
        treatment = credentials.treatments(entity).get(field)
        if treatment is None:
            raise OperationError(f"{entity.entity_name}.{field} is not a credential")

        table = mapping.table_for(entity)
        statement = _where(select(table.c[field]), entity, table, criteria).limit(1)
        stored = self._connection.execute(statement).scalar_one_or_none()
        return credentials.matches(candidate, stored, treatment)


def _where(statement, entity: type[Entity], table, criteria: Mapping[str, Any] | None):
    if not criteria:
        return statement
    _check_fields(entity, criteria, "select")
    for name, value in criteria.items():
        statement = statement.where(table.c[name] == value)
    return statement


def _stated_changes(entity: type[Entity], changes: Any) -> dict[str, Any]:
    """Only the fields a change actually states, empty ones included.

    A partial view keeps a field left out apart from one set to nothing, which
    is the difference between leaving a value alone and clearing it.
    """

    if isinstance(changes, PartialView):
        return changes.stated_fields()
    if isinstance(changes, Entity):
        return changes.model_dump(exclude_none=True)
    if isinstance(changes, Mapping):
        _check_fields(entity, changes, "change")
        return dict(entity.Partial.model_validate(dict(changes)).stated_fields())
    raise OperationError(f"{changes!r} is not a set of changes")


__all__ = [
    "DISABLE",
    "ENABLE",
    "OperationError",
    "Operations",
    "resolve_definition",
    "validate_stored",
]
