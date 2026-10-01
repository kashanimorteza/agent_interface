"""Published names of the Storage Actions, derived from Database's capability catalogue."""

from collections.abc import Iterable, Mapping
from typing import Final

from database.interface import Database

from logic.core.errors import ConfigurationError
from logic.core.identity import validate_identities

SERVICE_NAME: Final = "Storage"

ACTION_NAME_OVERRIDES: Final[Mapping[str, str]] = {}


def capabilities() -> tuple[str, ...]:
    """Return the capabilities Database currently publishes, in its own order."""
    return tuple(
        name
        for name, member in vars(Database).items()
        if not name.startswith("_") and callable(member)
    )


def published_names(
    overrides: Mapping[str, str] = ACTION_NAME_OVERRIDES,
) -> dict[str, str]:
    """Return the published Action name of every Database capability.

    A name is the Service name, one underscore, and the capability's own name unless
    an override replaces that base name. An override that names no current Database
    capability is rejected; it is never ignored.

    Args:
        overrides (Mapping[str, str]): Replacement base names by capability name.
    """
    catalogue = capabilities()
    unknown = sorted(set(overrides) - set(catalogue))
    if unknown:
        raise ConfigurationError(
            f"Action-name overrides name no capability Database publishes: {unknown}."
        )
    prefix = SERVICE_NAME.lower()
    return {name: f"{prefix}_{overrides.get(name, name)}" for name in catalogue}


def verify_exports(exports: Iterable[str], contracts: Iterable[str]) -> None:
    """Require valid, unique identities and exactly one Action per capability plus the contracts.

    Args:
        exports (Iterable[str]): The names the gateway publishes.
        contracts (Iterable[str]): The names of the republished Database contracts.
    """
    published = list(exports)
    names = published_names().values()
    prefix = f"{SERVICE_NAME.lower()}_"
    validate_identities([SERVICE_NAME])
    validate_identities(name.removeprefix(prefix) for name in names)
    validate_identities(names)
    validate_identities(published)
    expected = {*names, *contracts}
    missing = sorted(expected - set(published))
    extra = sorted(set(published) - expected)
    if missing or extra:
        raise ConfigurationError(
            f"The Storage gateway must publish exactly one Action for every Database "
            f"capability and the republished contracts; missing {missing}, unexpected {extra}."
        )
