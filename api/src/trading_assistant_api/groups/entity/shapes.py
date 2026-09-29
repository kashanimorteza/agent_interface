"""Entity Group shapes: the external request and response of every Endpoint.

Every shape follows the published Action contract. An input the Action declares with a plain
type (a record id, a Field name) is offered as a query input of that type; a record supplied to
`add` or `update` is a Transport Schema derived from the Fields of the Entity the Child Service is
bound to, so no Field is restated here. A result is a record, a collection of records, or the
plain value the Action declares.
"""

import inspect
import re
import typing
from enum import Enum, StrEnum
from functools import cache
from typing import Annotated, Any

from fastapi import Query
from pydantic import Field, create_model
from sqlmodel import SQLModel

from trading_assistant_api.core.endpoints import Endpoint
from trading_assistant_api.core.failures import FailureBody, RecordNotFound
from trading_assistant_api.core.queries import DEFAULT_LIMIT, MAXIMUM_LIMIT
from trading_assistant_api.groups.entity import adapter
from trading_assistant_api.groups.entity.credentials import withheld
from trading_assistant_api.groups.entity.router import Shape


class Transport(SQLModel):
    """Base of every Transport Schema: an input the schema does not declare is refused."""

    model_config = {"extra": "forbid"}


class InsufficientContract(ValueError):
    """A published Action contract cannot yield an external shape."""


RECORD = frozenset({"add", "update", "get_by_id", "enable", "disable"})
COLLECTION = frozenset({"list"})
PURPOSES = {
    "add": "Create a {label} record.",
    "update": "Replace every mutable Field of a {label} record.",
    "list": "List {label} records.",
    "get_by_id": "Retrieve one {label} record by its id.",
    "count": "Count {label} records.",
    "sum": "Total a Field over {label} records.",
    "min": "Find the smallest value of a Field over {label} records.",
    "max": "Find the largest value of a Field over {label} records.",
    "enable": "Mark a {label} record active.",
    "disable": "Mark a {label} record inactive.",
    "delete": "Delete a {label} record.",
    "truncate": "Delete every {label} record.",
}


def label(entity: type[Any]) -> str:
    """Return the readable name of an Entity, such as `Account Group`."""
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", entity.__name__)


def _schema(
    name: str, entity: type[Any], id_rule: str, withhold: tuple[str, ...] = ()
) -> Any:
    """Derive a Transport Schema from the Fields of an Entity.

    Args:
        name (str): Name of the schema.
        entity (type[Any]): Entity whose Fields the schema carries.
        id_rule (str): `omit` leaves out the generated id, `require` makes the id mandatory, and
            `keep` carries it as the Entity declares it.
        withhold (tuple[str, ...]): Fields the schema leaves out.

    Returns:
        (Any): A non-table SQLModel class.
    """
    fields: dict[str, Any] = {
        field: (info.annotation, info)
        for field, info in entity.model_fields.items()
        if field not in withhold and not (field == "id" and id_rule == "omit")
    }
    if id_rule == "require":
        fields["id"] = (int, Field())
    return create_model(name, __base__=Transport, **fields)


@cache
def schemas(child: str) -> tuple[Any, Any, Any]:
    """Return the record schemas of one Entity Child Service.

    Args:
        child (str): Child Service name published by Entity Service Interface.

    Returns:
        (tuple[Any, Any, Any]): The schema of a record to create, of a record to replace, and
            of a record in a response.
    """
    entity = adapter.entity_of(child)
    name = entity.__name__
    return (
        _schema(f"{name}Create", entity, "omit"),
        _schema(f"{name}Replace", entity, "require"),
        _schema(name, entity, "keep", withheld(entity)),
    )


def _query(name: str, hint: Any) -> inspect.Parameter:
    """Offer a plain-typed Action input as a required query input."""
    return inspect.Parameter(
        name, inspect.Parameter.KEYWORD_ONLY, annotation=Annotated[hint, Query()]
    )


def _page_size() -> inspect.Parameter:
    """Offer the bounded page size of a collection."""
    return inspect.Parameter(
        "limit",
        inspect.Parameter.KEYWORD_ONLY,
        default=DEFAULT_LIMIT,
        annotation=Annotated[int, Query(ge=1, le=MAXIMUM_LIMIT)],
    )


def _published_field(record: Any) -> inspect.Parameter:
    """Offer the Field an aggregate works on, limited to the Fields the resource publishes."""
    published = StrEnum(
        f"{record.__name__}Field", {name: name for name in record.model_fields}
    )
    return inspect.Parameter(
        "field",
        inspect.Parameter.KEYWORD_ONLY,
        annotation=Annotated[published, Query()],
    )


def _instance(hint: Any) -> inspect.Parameter | None:
    """Offer the Instance selection an Action declares, when its type is an enumeration."""
    members = [
        member
        for member in typing.get_args(hint)
        if inspect.isclass(member) and issubclass(member, Enum)
    ]
    if not members:
        return None
    return inspect.Parameter(
        "instance",
        inspect.Parameter.KEYWORD_ONLY,
        default=None,
        annotation=Annotated[members[0] | None, Query()],
    )


def _record(result: Any) -> Any:
    """Refuse a request that named a record which does not exist."""
    if result is None:
        raise RecordNotFound
    return result


def shape_of(endpoint: Endpoint) -> Shape:
    """Derive the external shape of an Endpoint from its published Action contract.

    Args:
        endpoint (Endpoint): An Endpoint of the Entity Group.

    Returns:
        (Shape): The request inputs, the response, and the mapping from the Action's result.

    Raises:
        InsufficientContract: When the Action contract cannot yield a shape; the message names
            the Endpoint.
    """
    child, _, kind = endpoint.identity.partition(".")
    action = adapter.resolve(endpoint.identity)
    hints = typing.get_type_hints(action)
    for name in inspect.signature(action).parameters:
        if name not in hints:
            raise InsufficientContract(
                f"{endpoint.identity} declares no type for its parameter {name}"
            )
    try:
        entity = adapter.entity_of(child)
    except AttributeError:
        raise InsufficientContract(
            f"{child} is not bound to an Entity, so {endpoint.identity} has no record shape"
        ) from None
    create, replace, record = schemas(child)
    parameters: list[inspect.Parameter] = []
    for name, hint in hints.items():
        if name == "return":
            continue
        if name == "entity":
            body = create if kind == "add" else replace
            parameters.append(
                inspect.Parameter(name, inspect.Parameter.KEYWORD_ONLY, annotation=body)
            )
        elif name == "limit":
            parameters.append(_page_size())
        elif name == "field" and hint is str:
            parameters.append(_published_field(record))
        elif hint in (int, str):
            parameters.append(_query(name, hint))
        elif name == "instance" and (selection := _instance(hint)):
            parameters.append(selection)
    failures: dict[int | str, dict[str, Any]] = {
        409: {"model": FailureBody, "description": "The request was refused."},
        422: {"model": FailureBody, "description": "The input violates the shape."},
        500: {"model": FailureBody, "description": "Unexpected failure."},
    }
    if kind in (RECORD | {"delete"}) - {"add"}:
        failures[404] = {"model": FailureBody, "description": "No such record."}
    documentation = {
        "summary": PURPOSES[kind].format(label=label(entity)),
        "responses": failures,
    }
    if kind in RECORD:
        return Shape(
            tuple(parameters),
            record,
            lambda result: record.model_validate(_record(result), from_attributes=True),
            201 if kind == "add" else 200,
            documentation,
        )
    if kind in COLLECTION:
        return Shape(
            tuple(parameters),
            list[record],
            lambda result: [
                record.model_validate(item, from_attributes=True) for item in result
            ],
            documentation=documentation,
        )
    if kind == "delete":
        return Shape(
            tuple(parameters),
            bool,
            lambda result: _record(result or None),
            documentation=documentation,
        )
    return Shape(
        tuple(parameters),
        hints["return"],
        documentation=documentation,
    )
