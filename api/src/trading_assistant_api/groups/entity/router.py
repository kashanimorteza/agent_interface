"""Entity Group Router: the HTTP-facing boundary of the one Entity Group.

Router owns the Group's route namespace, the method of every Endpoint, the external request and
response shapes, and the public representation of outcomes. It calls only its own Adapter and
holds no application Behaviour: an Endpoint forwards its validated input to the Adapter and
turns the Adapter's outcome into the response.
"""

import inspect
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from types import ModuleType
from typing import Any

from fastapi import APIRouter, Request
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel

from trading_assistant_api.core.endpoints import Endpoint
from trading_assistant_api.groups.entity import adapter as entity_adapter


def unchanged(result: Any) -> Any:
    """Return an Action's result as the response."""
    return result


@dataclass(frozen=True)
class Shape:
    """The external request and response of one Endpoint.

    Attributes:
        parameters (tuple[inspect.Parameter, ...]): Path, query, and body inputs; each is named
            as the Action parameter it is passed on as.
        response (Any): The declared type of the successful response.
        result (Callable[[Any], Any]): Maps the Action's result to the response.
        status (int): Status of a successful response.
        documentation (dict[str, Any]): Contract metadata such as the summary and the declared
            failures.
    """

    parameters: tuple[inspect.Parameter, ...] = ()
    response: Any = None
    result: Callable[[Any], Any] = unchanged
    status: int = 200
    documentation: dict[str, Any] = field(default_factory=dict)


class _Endpoint:
    """The function that serves one Endpoint: it forwards its input and shapes the outcome."""

    def __init__(self, identity: str, shape: Shape, adapter: ModuleType) -> None:
        """Bind an Endpoint to its Adapter.

        Args:
            identity (str): Action identity, `<Child Service>.<action>`.
            shape (Shape): External shape of the Endpoint.
            adapter (ModuleType): The Group's Adapter.
        """
        self.identity = identity
        self.shape = shape
        self.adapter = adapter
        self.__name__ = identity.replace(".", "_")
        self.inputs = {parameter.name for parameter in shape.parameters}
        self.__signature__ = inspect.Signature(
            [
                parameter.replace(kind=inspect.Parameter.KEYWORD_ONLY)
                for parameter in shape.parameters
            ]
            + [
                inspect.Parameter(
                    "request", inspect.Parameter.KEYWORD_ONLY, annotation=Request
                )
            ]
        )

    def __call__(self, **received: Any) -> Any:
        """Serve one request."""
        request = received.pop("request")
        undeclared = sorted(set(request.query_params) - self.inputs)
        if undeclared:
            raise RequestValidationError(
                [
                    {
                        "type": "extra_forbidden",
                        "loc": ("query", name),
                        "msg": "Extra inputs are not permitted",
                    }
                    for name in undeclared
                ]
            )
        arguments = {
            name: value.model_dump(exclude_unset=True)
            if isinstance(value, BaseModel)
            else value
            for name, value in received.items()
            if value is not None
        }
        return self.shape.result(self.adapter.call(self.identity, **arguments))


def create_router(
    group: str,
    endpoints: Iterable[Endpoint],
    shape_of: Callable[[Endpoint], Shape],
    adapter: ModuleType = entity_adapter,
) -> APIRouter:
    """Serve the Group's Endpoints under its route namespace.

    Args:
        group (str): Identity of the Group, its route namespace.
        endpoints (Iterable[Endpoint]): The Group's validated Endpoints.
        shape_of (Callable[[Endpoint], Shape]): External shape of an Endpoint.
        adapter (ModuleType): The Group's Adapter, the only thing Router calls.

    Returns:
        (APIRouter): Router that Bootstrap registers under the version prefix.
    """
    router = APIRouter(prefix=f"/{group}", tags=[group])
    for endpoint in endpoints:
        shape = shape_of(endpoint)
        router.add_api_route(
            endpoint.path.removeprefix(f"/{group}"),
            _Endpoint(endpoint.identity, shape, adapter),
            methods=[endpoint.method],
            response_model=shape.response,
            status_code=shape.status,
            **shape.documentation,
        )
    return router
