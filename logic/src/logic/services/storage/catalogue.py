"""Derivation of Storage Actions from the Operations Database Interface publishes."""

from collections.abc import Callable, Iterable
from importlib import import_module
from importlib.util import find_spec
from typing import Any

from logic.core.errors import ConfigurationError
from logic.core.identifiers import check_identifiers, snake_case
from logic.core.settings import ServiceSettings
from logic.services.storage import gateway

_ACTIONS_PACKAGE = "logic.services.storage.actions"


def operations(database: type) -> tuple[str, ...]:
    """Return the Operations a Database access surface publishes.

    Args:
        database (type): Database access surface whose public methods are its Operations.

    Returns:
        (tuple[str, ...]): Stable Operation identities in publication order.
    """
    return tuple(
        name
        for name, member in vars(database).items()
        if not name.startswith("_") and callable(member)
    )


def action_name(service: ServiceSettings, operation: str) -> str:
    """Return the published Action name of an Operation.

    Args:
        service (ServiceSettings): Storage Service settings.
        operation (str): Stable Operation identity.

    Returns:
        (str): The configured Service name, one underscore, and the derived or overridden base name.
    """
    return f"{snake_case(service.name)}_{snake_case(service.action_names.get(operation, operation))}"


def _forwarder(operation: str, name: str) -> Callable[..., Any]:
    def action(*args: Any, **kwargs: Any) -> Any:
        return getattr(gateway.database(), operation)(*args, **kwargs)

    action.__name__ = name
    action.__doc__ = f"Forward the {operation} Operation to Database unchanged."
    return action


def derive(
    database: type, service: ServiceSettings, reserved: Iterable[str] = ()
) -> dict[str, Callable[..., Any]]:
    """Derive exactly one Action for every Operation the Database access surface publishes.

    Args:
        database (type): Database access surface whose public methods are its Operations.
        service (ServiceSettings): Storage Service settings, including Action-name overrides.
        reserved (Iterable[str]): Other public exports the Actions must not collide with.

    Returns:
        (dict[str, Callable[..., Any]]): Actions by published name; a written Action file is used
            when it exists, otherwise a forwarding Action is derived.
    """
    catalogue = operations(database)
    unknown = sorted(set(service.action_names) - set(catalogue))
    if unknown:
        raise ConfigurationError(
            f"Action-name overrides name unknown Operations: {', '.join(unknown)}"
        )
    names = {operation: action_name(service, operation) for operation in catalogue}
    check_identifiers([*names.values(), *reserved], "Storage export")
    actions: dict[str, Callable[..., Any]] = {}
    for operation, name in names.items():
        module = f"{_ACTIONS_PACKAGE}.{name}"
        actions[name] = (
            getattr(import_module(module), name)
            if find_spec(module)
            else _forwarder(operation, name)
        )
    return actions
