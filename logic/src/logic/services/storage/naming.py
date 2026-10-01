"""Published names of the Storage gateway, read from what Database Interface publishes."""

import inspect
from collections.abc import Iterable
from typing import Final

import database.interface as _database_interface
from database.interface import Database

from logic.core.errors import ConfigurationError
from logic.core.identity import validate_identities

SERVICE_NAME: Final = "Storage"


def capabilities() -> tuple[str, ...]:
    """Return the capabilities Database currently publishes, in its own order."""
    return tuple(
        name
        for name, member in vars(Database).items()
        if not name.startswith("_") and callable(member)
    )


def action_names() -> dict[str, str]:
    """Return the Action name of every Database capability: the Service name, one underscore, the capability name."""
    prefix = SERVICE_NAME.lower()
    return {name: f"{prefix}_{name}" for name in capabilities()}


def contracts() -> tuple[str, ...]:
    """Return every supporting contract Database Interface publishes: each public class it defines except Database."""
    return tuple(
        name
        for name, member in vars(_database_interface).items()
        if not name.startswith("_")
        and inspect.isclass(member)
        and member.__module__ == _database_interface.__name__
        and member is not Database
    )


def verify_exports(exports: Iterable[str]) -> None:
    """Require valid, unique identities and exactly one Action per capability plus every published contract.

    Args:
        exports (Iterable[str]): The names the gateway publishes.
    """
    published = list(exports)
    names = action_names().values()
    validate_identities([SERVICE_NAME])
    validate_identities(names)
    validate_identities(published)
    expected = {*names, *contracts()}
    missing = sorted(expected - set(published))
    extra = sorted(set(published) - expected)
    if missing or extra:
        raise ConfigurationError(
            f"The Storage gateway must publish exactly one Action for every Database "
            f"capability and every contract Database publishes; missing {missing}, unexpected {extra}."
        )
