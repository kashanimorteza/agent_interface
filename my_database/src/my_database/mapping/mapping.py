"""Mapping: resolves each request's Database Instance and Engine, routes the request, and standardizes the result."""

from collections.abc import Callable
from typing import Any

from sqlmodel import SQLModel

from my_database.configuration import Configuration
from my_database.engine import SqliteEngine
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
    ReportRequest,
    Request,
    Result,
    UpdateRequest,
)

ENGINES = {"sqlite": SqliteEngine}


class Mapping:
    """Routes Operation requests to the Engine of their Database Instance.

    Attributes:
        configuration (Configuration): The Database Configuration that declares Engines and Database Instances.
    """

    def __init__(self, configuration: Configuration):
        """Prepare routing over a Database Configuration.

        Args:
            configuration (Configuration): Database Configuration declaring Engines, Database Instances, and Settings.
        """
        self.configuration = configuration
        self.reports: dict[str, Callable[..., Any]] = {}
        self.commands: dict[str, Callable[..., Any]] = {}
        self._engines: dict[str, SqliteEngine] = {}

    def resolve(self, instance: str | None) -> SqliteEngine | None:
        """Resolve the Engine serving a Database Instance.

        Args:
            instance (str | None): Database Instance key or purpose key; the default Database Instance when None.

        Returns:
            (SqliteEngine | None): The Engine of the resolved Database Instance; None when the name is not declared.
        """
        settings = self.configuration.settings
        key = settings.assignments.get(
            instance or "", instance or settings.default_instance
        )
        if key not in self.configuration.instances:
            return None
        if key not in self._engines:
            declared = self.configuration.instances[key]
            self._engines[key] = ENGINES[declared.engine](self.configuration, declared)
        return self._engines[key]

    def route(self, operation: str, request: Request, *extra: Any) -> Result[Any]:
        """Forward a request to the Engine of its Database Instance and return the standardized result.

        Args:
            operation (str): Name of the Engine behaviour that carries out the Operation.
            request (Request): The Operation request.
            *extra (Any): Further arguments the Engine behaviour takes after the request.

        Returns:
            (Result[Any]): The Engine's result; a failure when the Database Instance is not declared.
        """
        engine = self.resolve(request.instance)
        if engine is None:
            return Result(
                Outcome.FAILURE,
                message=f"Database Instance '{request.instance}' is not declared.",
            )
        answer = getattr(engine, operation)(request, *extra)
        return answer if isinstance(answer, Result) else Result(Outcome.SUCCESS, answer)

    def add(self, request: AddRequest) -> Result[SQLModel]:
        """Route an Add request to its Engine."""
        return self.route("add", request)

    def edit(self, request: EditRequest) -> Result[dict[str, Any]]:
        """Route an Edit request to its Engine."""
        return self.route("edit", request)

    def update(self, request: UpdateRequest) -> Result[SQLModel]:
        """Route an Update request to its Engine."""
        return self.route("update", request)

    def list_(self, request: ListRequest) -> Result[list[SQLModel]]:
        """Route a List request to its Engine."""
        return self.route("list_", request)

    def delete(self, request: DeleteRequest) -> Result[None]:
        """Route a Delete request to its Engine."""
        return self.route("delete", request)

    def enable(self, request: EnableRequest) -> Result[SQLModel]:
        """Route an Enable request to its Engine."""
        return self.route("enable", request)

    def disable(self, request: DisableRequest) -> Result[SQLModel]:
        """Route a Disable request to its Engine."""
        return self.route("disable", request)

    def get_by_id(self, request: GetRequest) -> Result[SQLModel]:
        """Route a Get by ID request to its Engine."""
        return self.route("get_by_id", request)

    def report(self, request: ReportRequest) -> Result[Any]:
        """Route a Report request to its Engine together with the declared report it names."""
        if request.name not in self.reports:
            return Result(
                Outcome.FAILURE, message=f"Report '{request.name}' is not declared."
            )
        return self.route("report", request, self.reports[request.name])

    def execute_command(self, request: CommandRequest) -> Result[Any]:
        """Route an Execute Command request to its Engine together with the declared command it names."""
        if request.name not in self.commands:
            return Result(
                Outcome.FAILURE, message=f"Command '{request.name}' is not declared."
            )
        return self.route("execute_command", request, self.commands[request.name])
