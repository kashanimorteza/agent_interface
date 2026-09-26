"""Interface: the public entry point through which Logic requests Database Operations."""

from collections.abc import Callable
from typing import Any

from sqlmodel import SQLModel

from my_database.configuration import Configuration
from my_database.mapping import Mapping
from my_database.standard import (
    AddRequest,
    CommandRequest,
    DeleteRequest,
    DisableRequest,
    EditRequest,
    EnableRequest,
    GetRequest,
    ListRequest,
    ReportRequest,
    Result,
    UpdateRequest,
)


class Interface:
    """Receives Operation requests and returns their results in the standard form.

    Attributes:
        mapping (Mapping): The routing layer that serves every request.
    """

    def __init__(self, configuration: Configuration | None = None):
        """Prepare the Operations over a Database Configuration.

        Args:
            configuration (Configuration, optional): Database Configuration; loaded from its default location when omitted.
        """
        self.mapping = Mapping(configuration or Configuration.load())

    def add(self, record: SQLModel, *, instance: str | None = None) -> Result[SQLModel]:
        """Store a new record.

        Args:
            record (SQLModel): Entity instance holding the new record's values.
            instance (str | None): Database Instance key; the default Database Instance when None.

        Returns:
            (Result[SQLModel]): The created record, or a failure when a declared rule is broken.
        """
        return self.mapping.add(AddRequest(record=record, instance=instance))

    def edit(
        self, entity: type[SQLModel], record_id: int, *, instance: str | None = None
    ) -> Result[dict[str, Any]]:
        """Return a record in editable form.

        Args:
            entity (type[SQLModel]): Entity class of the record.
            record_id (int): Identifier of the record.
            instance (str | None): Database Instance key; the default Database Instance when None.

        Returns:
            (Result[dict[str, Any]]): The record's Field values, or not found.
        """
        return self.mapping.edit(
            EditRequest(entity=entity, record_id=record_id, instance=instance)
        )

    def update(
        self, record: SQLModel, *, instance: str | None = None
    ) -> Result[SQLModel]:
        """Store changed values on an existing record.

        Args:
            record (SQLModel): Entity instance holding the record identifier and the changed values.
            instance (str | None): Database Instance key; the default Database Instance when None.

        Returns:
            (Result[SQLModel]): The updated record, not found, or a failure when a declared rule is broken.
        """
        return self.mapping.update(UpdateRequest(record=record, instance=instance))

    def list_(
        self,
        entity: type[SQLModel],
        filters: dict[str, Any] | None = None,
        order_by: tuple[str, ...] = (),
        *,
        instance: str | None = None,
    ) -> Result[list[SQLModel]]:
        """List the records of an Entity.

        Args:
            entity (type[SQLModel]): Entity class to list.
            filters (dict[str, Any], optional): Field name to the value a record must hold.
            order_by (tuple[str, ...]): Field names to order by; a leading '-' orders descending.
            instance (str | None): Database Instance key; the default Database Instance when None.

        Returns:
            (Result[list[SQLModel]]): The matching records, or a failure naming an unknown Field.
        """
        return self.mapping.list_(
            ListRequest(
                entity=entity,
                filters=filters or {},
                order_by=order_by,
                instance=instance,
            )
        )

    def delete(
        self, entity: type[SQLModel], record_id: int, *, instance: str | None = None
    ) -> Result[None]:
        """Remove a record.

        Args:
            entity (type[SQLModel]): Entity class of the record.
            record_id (int): Identifier of the record.
            instance (str | None): Database Instance key; the default Database Instance when None.

        Returns:
            (Result[None]): Success, not found, or a failure when other records still reference the record.
        """
        return self.mapping.delete(
            DeleteRequest(entity=entity, record_id=record_id, instance=instance)
        )

    def enable(
        self, entity: type[SQLModel], record_id: int, *, instance: str | None = None
    ) -> Result[SQLModel]:
        """Mark a record active.

        Args:
            entity (type[SQLModel]): Entity class of the record.
            record_id (int): Identifier of the record.
            instance (str | None): Database Instance key; the default Database Instance when None.

        Returns:
            (Result[SQLModel]): The enabled record, or not found.
        """
        return self.mapping.enable(
            EnableRequest(entity=entity, record_id=record_id, instance=instance)
        )

    def disable(
        self, entity: type[SQLModel], record_id: int, *, instance: str | None = None
    ) -> Result[SQLModel]:
        """Mark a record inactive.

        Args:
            entity (type[SQLModel]): Entity class of the record.
            record_id (int): Identifier of the record.
            instance (str | None): Database Instance key; the default Database Instance when None.

        Returns:
            (Result[SQLModel]): The disabled record, or not found.
        """
        return self.mapping.disable(
            DisableRequest(entity=entity, record_id=record_id, instance=instance)
        )

    def get_by_id(
        self, entity: type[SQLModel], record_id: int, *, instance: str | None = None
    ) -> Result[SQLModel]:
        """Return one record by identifier.

        Args:
            entity (type[SQLModel]): Entity class of the record.
            record_id (int): Identifier of the record.
            instance (str | None): Database Instance key; the default Database Instance when None.

        Returns:
            (Result[SQLModel]): The matching record, or not found.
        """
        return self.mapping.get_by_id(
            GetRequest(entity=entity, record_id=record_id, instance=instance)
        )

    def declare_report(self, name: str, handler: Callable[..., Any]) -> None:
        """Declare a report that Report can produce.

        Args:
            name (str): Report name.
            handler (Callable[..., Any]): Called with a session and the selection criteria as keyword arguments.
        """
        self.mapping.reports[name] = handler

    def report(
        self,
        name: str,
        criteria: dict[str, Any] | None = None,
        *,
        instance: str | None = None,
    ) -> Result[Any]:
        """Produce a declared report.

        Args:
            name (str): Name of the declared report.
            criteria (dict[str, Any], optional): Report-specific selection criteria.
            instance (str | None): Database Instance key; the default Database Instance when None.

        Returns:
            (Result[Any]): The report, or a failure when it is not declared or the criteria do not fit it.
        """
        return self.mapping.report(
            ReportRequest(name=name, criteria=criteria or {}, instance=instance)
        )

    def declare_command(self, name: str, handler: Callable[..., Any]) -> None:
        """Declare a database command that Execute Command can run.

        Args:
            name (str): Command name.
            handler (Callable[..., Any]): Called with a session and the parameters as keyword arguments.
        """
        self.mapping.commands[name] = handler

    def execute_command(
        self,
        name: str,
        parameters: dict[str, Any] | None = None,
        *,
        instance: str | None = None,
    ) -> Result[Any]:
        """Run a declared database command, which need not concern one Model.

        Args:
            name (str): Name of the declared command.
            parameters (dict[str, Any], optional): Parameters supplied to the command.
            instance (str | None): Database Instance key; the default Database Instance when None.

        Returns:
            (Result[Any]): The command's result, or a failure when it is not declared or the parameters do not fit it.
        """
        return self.mapping.execute_command(
            CommandRequest(name=name, parameters=parameters or {}, instance=instance)
        )
