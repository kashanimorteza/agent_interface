"""Operation request and result standard shared by Interface, Mapping, and every Engine.

Every published Operation is requested with one Request and answered with one Result.

Outcomes by Operation:
    Add: SUCCESS with the created record; FAILURE when a declared constraint is broken.
    Edit: SUCCESS with the record's Field values as an editable dict; NOT_FOUND.
    Update: SUCCESS with the updated record; NOT_FOUND; FAILURE when a declared constraint is broken.
    List: SUCCESS with the matching records; FAILURE for an unknown Field.
    Delete: SUCCESS; NOT_FOUND (nothing removed); FAILURE when other records still reference the record.
    Enable, Disable: SUCCESS with the changed record; NOT_FOUND.
    Get by ID: SUCCESS with the record; NOT_FOUND.
    Report, Execute Command: SUCCESS with the report or command result; FAILURE when not declared or not runnable.
Any Operation also answers FAILURE when its Database Instance is not declared.
"""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from sqlmodel import SQLModel


class Outcome(StrEnum):
    """How an Operation ended."""

    SUCCESS = "success"
    NOT_FOUND = "not_found"
    FAILURE = "failure"


@dataclass(frozen=True, slots=True)
class Result[T]:
    """The answer to one Operation request.

    Attributes:
        outcome (Outcome): How the Operation ended.
        value (T | None): The record, records, or result the Operation returns; None when it returns nothing.
        message (str): Human-readable explanation of the outcome.
    """

    outcome: Outcome
    value: T | None = None
    message: str = ""

    @property
    def ok(self) -> bool:
        """Whether the Operation succeeded."""
        return self.outcome is Outcome.SUCCESS


@dataclass(frozen=True, slots=True, kw_only=True)
class Request:
    """Common part of every Operation request.

    Attributes:
        instance (str | None): Key of the Database Instance to use; the default Database Instance when None.
    """

    instance: str | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class AddRequest(Request):
    """Request to store a new record.

    Attributes:
        record (SQLModel): Entity instance holding the new record's values.
    """

    record: SQLModel


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateRequest(Request):
    """Request to store changed values on an existing record.

    Attributes:
        record (SQLModel): Entity instance holding the record identifier and the changed values.
    """

    record: SQLModel


@dataclass(frozen=True, slots=True, kw_only=True)
class ListRequest(Request):
    """Request for the records of an Entity.

    Attributes:
        entity (type[SQLModel]): Entity class to list.
        filters (dict[str, Any]): Field name to the value a record must hold.
        order_by (tuple[str, ...]): Field names to order by; a leading '-' orders descending.
    """

    entity: type[SQLModel]
    filters: dict[str, Any] = field(default_factory=dict)
    order_by: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True, kw_only=True)
class RecordRequest(Request):
    """Request addressing one record by Entity class and identifier.

    Attributes:
        entity (type[SQLModel]): Entity class of the record.
        record_id (int): Identifier of the record.
    """

    entity: type[SQLModel]
    record_id: int


@dataclass(frozen=True, slots=True, kw_only=True)
class EditRequest(RecordRequest):
    """Request for a record in editable form."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteRequest(RecordRequest):
    """Request to remove a record."""


@dataclass(frozen=True, slots=True, kw_only=True)
class EnableRequest(RecordRequest):
    """Request to mark a record active."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DisableRequest(RecordRequest):
    """Request to mark a record inactive."""


@dataclass(frozen=True, slots=True, kw_only=True)
class GetRequest(RecordRequest):
    """Request for one record by identifier."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ReportRequest(Request):
    """Request for a declared report.

    Attributes:
        name (str): Name of the declared report.
        criteria (dict[str, Any]): Report-specific selection criteria.
    """

    name: str
    criteria: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True, kw_only=True)
class CommandRequest(Request):
    """Request to run a declared database command.

    Attributes:
        name (str): Name of the declared command.
        parameters (dict[str, Any]): Parameters supplied to the command.
    """

    name: str
    parameters: dict[str, Any] = field(default_factory=dict)


OPERATIONS: dict[str, type[Request]] = {
    "add": AddRequest,
    "edit": EditRequest,
    "update": UpdateRequest,
    "list": ListRequest,
    "delete": DeleteRequest,
    "enable": EnableRequest,
    "disable": DisableRequest,
    "get": GetRequest,
    "report": ReportRequest,
    "execute_command": CommandRequest,
}
