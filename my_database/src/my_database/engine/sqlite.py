"""SQLite Engine: storage behaviour for Database Instances that use the sqlite Engine."""

import inspect
from collections.abc import Callable
from pathlib import Path
from typing import Any

from pydantic import ValidationError
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, SQLModel, create_engine, select

from my_database.configuration import Configuration, InstanceConfiguration
from my_database.protection import Protection
from my_database.schema import metadata
from my_database.standard import (
    AddRequest,
    CommandRequest,
    DeleteRequest,
    DisableRequest,
    EditRequest,
    EnableRequest,
    GetRequest,
    ListRequest,
    Outcome,
    RecordRequest,
    ReportRequest,
    Result,
    UpdateRequest,
)


class SqliteEngine:
    """Storage behaviour of one Database Instance stored in a SQLite database.

    Attributes:
        configuration (Configuration): The Database Configuration the Engine is declared in.
        instance (InstanceConfiguration): The Database Instance this Engine serves.
        protection (Protection): At-rest protection applied to every stored credential.
        engine (Engine): SQLAlchemy engine holding the connection to the storage.
    """

    def __init__(self, configuration: Configuration, instance: InstanceConfiguration):
        """Open the storage of a Database Instance.

        Args:
            configuration (Configuration): Database Configuration declaring the Engine and the Database Instance.
            instance (InstanceConfiguration): Database Instance served by this Engine.
        """
        parameters: dict[str, Any] = configuration.engines[instance.engine].parameters
        location = configuration.directory / instance.path
        Path(location).parent.mkdir(parents=True, exist_ok=True)
        self.configuration = configuration
        self.instance = instance
        self.protection = Protection(configuration)
        self.engine = create_engine(
            f"sqlite:///{location}",
            connect_args={"check_same_thread": parameters["check_same_thread"]},
        )
        if parameters["foreign_keys"]:
            event.listen(self.engine, "connect", _enable_foreign_keys)

    def create_tables(self) -> None:
        """Create a Table for every Entity in the storage from the Entity metadata; existing Tables are kept."""
        metadata().create_all(self.engine)

    def session(self) -> Session:
        """Open a session on the storage.

        Returns:
            (Session): A session that keeps returned records readable after it closes.
        """
        return Session(self.engine, expire_on_commit=False)

    def add(self, request: AddRequest) -> Result[SQLModel]:
        """Store a new record.

        Args:
            request (AddRequest): Request holding the Entity instance to store.

        Returns:
            (Result[SQLModel]): The created record, or a failure when a declared rule is broken.
        """
        entity = type(request.record)
        with self.session() as session:
            try:
                record = entity.model_validate(
                    self.protection.protect(entity, request.record.model_dump())
                )
                session.add(record)
                session.commit()
            except (ValidationError, IntegrityError) as error:
                return Result(Outcome.FAILURE, message=str(error).splitlines()[0])
            session.refresh(record)
            return Result(Outcome.SUCCESS, record)

    def edit(self, request: EditRequest) -> Result[dict[str, Any]]:
        """Return a record in editable form.

        Args:
            request (EditRequest): Request holding the Entity class and record identifier.

        Returns:
            (Result[dict[str, Any]]): The record's Field values, or not found.
        """
        with self.session() as session:
            record = session.get(request.entity, request.record_id)
            return (
                _not_found(request)
                if record is None
                else Result(Outcome.SUCCESS, record.model_dump())
            )

    def update(self, request: UpdateRequest) -> Result[SQLModel]:
        """Store changed values on an existing record.

        Args:
            request (UpdateRequest): Request holding an Entity instance with the record identifier and the changed values.

        Returns:
            (Result[SQLModel]): The updated record, not found, or a failure when a declared rule is broken.
        """
        entity = type(request.record)
        record_id = getattr(request.record, "id", None)
        changes = self.protection.protect(
            entity, request.record.model_dump(exclude_unset=True, exclude={"id"})
        )
        with self.session() as session:
            stored = None if record_id is None else session.get(entity, record_id)
            if stored is None:
                return Result(
                    Outcome.NOT_FOUND,
                    message=f"{entity.__name__} {record_id} was not found.",
                )
            try:
                entity.model_validate({**stored.model_dump(), **changes})
                stored.sqlmodel_update(changes)
                session.commit()
            except (ValidationError, IntegrityError) as error:
                return Result(Outcome.FAILURE, message=str(error).splitlines()[0])
            session.refresh(stored)
            return Result(Outcome.SUCCESS, stored)

    def list_(self, request: ListRequest) -> Result[list[SQLModel]]:
        """Return the matching records of an Entity.

        Args:
            request (ListRequest): Request holding the Entity class, filters, and ordering.

        Returns:
            (Result[list[SQLModel]]): The matching records, or a failure naming an unknown Field.
        """
        entity = request.entity
        names = [*request.filters, *(name.lstrip("-") for name in request.order_by)]
        if unknown := [name for name in names if name not in entity.model_fields]:
            return Result(
                Outcome.FAILURE,
                message=f"{entity.__name__} has no Field {', '.join(unknown)}.",
            )
        statement = select(entity)
        for name, value in request.filters.items():
            statement = statement.where(getattr(entity, name) == value)
        for name in request.order_by:
            column = getattr(entity, name.lstrip("-"))
            statement = statement.order_by(
                column.desc() if name.startswith("-") else column
            )
        with self.session() as session:
            return Result(Outcome.SUCCESS, list(session.exec(statement).all()))

    def delete(self, request: DeleteRequest) -> Result[None]:
        """Remove a record.

        Args:
            request (DeleteRequest): Request holding the Entity class and record identifier.

        Returns:
            (Result[None]): Success, not found, or a failure when other records still reference the record.
        """
        with self.session() as session:
            record = session.get(request.entity, request.record_id)
            if record is None:
                return _not_found(request, " Nothing was removed.")
            try:
                session.delete(record)
                session.commit()
            except IntegrityError:
                return Result(
                    Outcome.FAILURE,
                    message=f"{request.entity.__name__} {request.record_id} is still referenced by other records. Nothing was removed.",
                )
            return Result(
                Outcome.SUCCESS,
                message=f"{request.entity.__name__} {request.record_id} was deleted.",
            )

    def enable(self, request: EnableRequest) -> Result[SQLModel]:
        """Mark a record active.

        Args:
            request (EnableRequest): Request holding the Entity class and record identifier.

        Returns:
            (Result[SQLModel]): The enabled record, or not found.
        """
        return self._set_active(request, True)

    def disable(self, request: DisableRequest) -> Result[SQLModel]:
        """Mark a record inactive.

        Args:
            request (DisableRequest): Request holding the Entity class and record identifier.

        Returns:
            (Result[SQLModel]): The disabled record, or not found.
        """
        return self._set_active(request, False)

    def get_by_id(self, request: GetRequest) -> Result[SQLModel]:
        """Return one record by identifier.

        Args:
            request (GetRequest): Request holding the Entity class and record identifier.

        Returns:
            (Result[SQLModel]): The matching record, or not found.
        """
        with self.session() as session:
            record = session.get(request.entity, request.record_id)
            return (
                _not_found(request)
                if record is None
                else Result(Outcome.SUCCESS, record)
            )

    def _set_active(self, request: RecordRequest, active: bool) -> Result[SQLModel]:
        with self.session() as session:
            record = session.get(request.entity, request.record_id)
            if record is None:
                return _not_found(request, " Nothing was changed.")
            record.is_active = active  # type: ignore[attr-defined]  # every Entity declares is_active
            session.commit()
            session.refresh(record)
            return Result(Outcome.SUCCESS, record)

    def report(
        self, request: ReportRequest, handler: Callable[..., Any]
    ) -> Result[Any]:
        """Produce a declared report.

        Args:
            request (ReportRequest): Request holding the selection criteria.
            handler (Callable[..., Any]): Declared report, called with a session and the criteria as keyword arguments.

        Returns:
            (Result[Any]): The report, or a failure when the criteria do not fit the declared report.
        """
        return self._run(handler, request.criteria)

    def execute_command(
        self, request: CommandRequest, handler: Callable[..., Any]
    ) -> Result[Any]:
        """Run a declared database command.

        Args:
            request (CommandRequest): Request holding the command parameters.
            handler (Callable[..., Any]): Declared command, called with a session and the parameters as keyword arguments.

        Returns:
            (Result[Any]): The command's result, or a failure when the parameters do not fit the declared command.
        """
        return self._run(handler, request.parameters)

    def _run(
        self, handler: Callable[..., Any], arguments: dict[str, Any]
    ) -> Result[Any]:
        with self.session() as session:
            try:
                inspect.signature(handler).bind(session, **arguments)
            except TypeError as error:
                return Result(
                    Outcome.FAILURE, message=f"Arguments not accepted: {error}"
                )
            return Result(Outcome.SUCCESS, handler(session, **arguments))


def _not_found(request: RecordRequest, note: str = "") -> Result[Any]:
    return Result(
        Outcome.NOT_FOUND,
        message=f"{request.entity.__name__} {request.record_id} was not found.{note}",
    )


def _enable_foreign_keys(connection: Any, _record: Any) -> None:
    connection.execute("PRAGMA foreign_keys=ON")
