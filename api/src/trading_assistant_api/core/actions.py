"""Endpoint membership: which callable Actions of an eligible Service become Endpoints.

The published Service Interface is the only source of Actions. A function it exports is an
Action, and so is every public classmethod of a class it exports (an Entity Child Service);
enums, constants, and other support exports never are.
"""

import inspect
from collections.abc import Callable, Collection
from enum import Enum
from types import ModuleType
from typing import Any


def callable_actions(interface: ModuleType) -> dict[str, Callable[..., Any]]:
    """Return every callable Action a Service Interface publishes.

    Args:
        interface (ModuleType): Service Interface published through Logic Interface.

    Returns:
        (dict[str, Callable[..., Any]]): Actions keyed by identity: the function name, or
            `<Export>.<action>` for an Action of an exported class.
    """
    actions: dict[str, Callable[..., Any]] = {}
    for name in interface.__all__:
        export = getattr(interface, name)
        if inspect.isfunction(export):
            actions[name] = export
        elif inspect.isclass(export) and not issubclass(export, Enum):
            for action, function in inspect.getmembers(export, inspect.ismethod):
                if not action.startswith("_"):
                    actions[f"{name}.{action}"] = function
    return actions


def api_actions(
    interface: ModuleType, disabled: Collection[str] = ()
) -> dict[str, Callable[..., Any]]:
    """Return the callable Actions that become Endpoints.

    Args:
        interface (ModuleType): Service Interface published through Logic Interface.
        disabled (Collection[str]): Identities of Actions that set `generate_api` to false in
            their owning Service.

    Returns:
        (dict[str, Callable[..., Any]]): Every published callable Action except the disabled.

    Raises:
        ValueError: When a disabled identity is not a published callable Action; the message
            names it.
    """
    actions = callable_actions(interface)
    for identity in disabled:
        if identity not in actions:
            raise ValueError(
                f"Action {identity} disables API generation but is not published"
            )
    return {name: fn for name, fn in actions.items() if name not in disabled}
