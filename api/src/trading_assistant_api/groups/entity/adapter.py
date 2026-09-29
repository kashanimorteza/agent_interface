"""Entity Group Adapter: carries validated input to Entity Service and its outcome back.

Adapter reaches only Entity Service, and only through Logic Interface. It holds no transport,
application decision, or persistence work: results pass back unchanged, and a refusal an
Action declares (a `ValueError`) becomes a `DeclaredFailure` for Router to represent. Any
other failure is unexpected and propagates untouched.
"""

import inspect
from collections.abc import Callable, Collection, Mapping
from enum import Enum
from typing import Any

from logic import interface as logic
from pydantic import ValidationError

from trading_assistant_api.core.actions import api_actions
from trading_assistant_api.core.failures import DeclaredFailure

DISABLED_ACTIONS: frozenset[str] = frozenset()


def actions(
    disabled: Collection[str] = DISABLED_ACTIONS,
) -> dict[str, Callable[..., Any]]:
    """Return every API-enabled callable Action of Entity Service.

    Args:
        disabled (Collection[str]): Identities that disable API generation in Entity Service.

    Returns:
        (dict[str, Callable[..., Any]]): Actions keyed by identity, `<Child Service>.<action>`.
    """
    return api_actions(logic.Entity, disabled)


def children() -> tuple[str, ...]:
    """Return the Child Services Entity Service Interface publishes.

    Returns:
        (tuple[str, ...]): Names of the exported classes that are not enumerations.
    """
    return tuple(
        name
        for name in logic.Entity.__all__
        if inspect.isclass(export := getattr(logic.Entity, name))
        and not issubclass(export, Enum)
    )


def resolve(
    identity: str, disabled: Collection[str] = DISABLED_ACTIONS
) -> Callable[..., Any]:
    """Return one API-enabled callable Action of Entity Service.

    Args:
        identity (str): Action identity, `<Child Service>.<action>`.
        disabled (Collection[str]): Identities that disable API generation in Entity Service.

    Returns:
        (Callable[..., Any]): The Action published by Entity Service Interface.

    Raises:
        ValueError: When the identity is not an API-enabled callable Action; the message names
            it.
    """
    enabled = actions(disabled)
    if identity not in enabled:
        raise ValueError(
            f"Action {identity} is not an API-enabled Action of Entity Service"
        )
    return enabled[identity]


def invoke(action: Callable[..., Any], **arguments: Any) -> Any:
    """Call an Entity Service Action and return its declared outcome.

    Args:
        action (Callable[..., Any]): Action returned by `resolve`.
        **arguments (Any): Validated input mapped to the Action's parameters.

    Returns:
        (Any): The Action's result, unchanged.

    Raises:
        DeclaredFailure: When the Action refuses the request with a `ValueError`.
    """
    try:
        return action(**arguments)
    except ValueError as refusal:
        raise DeclaredFailure(str(refusal)) from refusal


def entity_of(child: str) -> type[Any]:
    """Return the Model Entity class a Child Service of Entity Service is bound to.

    Args:
        child (str): Child Service name published by Entity Service Interface.

    Returns:
        (type[Any]): The bound Entity class, read from the published Child Service.
    """
    return getattr(logic.Entity, child).entity


def call(identity: str, **arguments: Any) -> Any:
    """Carry one request to the matching Entity Service Action and return its outcome.

    Args:
        identity (str): Action identity, `<Child Service>.<action>`.
        **arguments (Any): Validated input named as the Action's parameters. An `entity`
            mapping becomes an instance of the Child Service's Entity.

    Returns:
        (Any): The Action's result, unchanged.

    Raises:
        DeclaredFailure: When the Entity or the Action refuses the request; the message names
            the rule and never repeats a supplied value.
    """
    action = resolve(identity)
    if isinstance(arguments.get("entity"), Mapping):
        entity = entity_of(identity.partition(".")[0])
        try:
            arguments["entity"] = entity(**arguments["entity"])
        except ValidationError as refusal:
            raise DeclaredFailure(
                "; ".join(
                    f"{'.'.join(map(str, error['loc']))}: {error['msg']}"
                    for error in refusal.errors()
                )
            ) from refusal
        except ValueError as refusal:
            raise DeclaredFailure(str(refusal)) from refusal
    return invoke(action, **arguments)
