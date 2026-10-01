"""The Services of Logic and the publication settings the root Interface follows."""

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Final

from logic.core.errors import ConfigurationError
from logic.core.identity import validate_identities


@dataclass(frozen=True)
class ServiceSettings:
    """One Service's identity and its two independent settings.

    Attributes:
        role (str): The fixed role of the Service inside Logic.
        name (str): The configured name the Service is published under.
        directory (str): The configured name of the Service's own location.
        publish_in_logic_interface (bool): Whether the root Interface publishes the Service Interface.
        generate_api (bool): Whether the Service asks for one API Group; needs publication.
    """

    role: str
    name: str
    directory: str
    publish_in_logic_interface: bool
    generate_api: bool


SERVICES: Final = (
    ServiceSettings("entity", "Entity", "entity", True, True),
    ServiceSettings("storage", "Storage", "storage", False, False),
)


def published_names(services: Sequence[ServiceSettings] = SERVICES) -> tuple[str, ...]:
    """Return the names of the Services whose Interface the root Interface publishes.

    Args:
        services (Sequence[ServiceSettings]): The Services and their settings.
    """
    return tuple(
        service.name for service in services if service.publish_in_logic_interface
    )


def api_eligible_names(
    services: Sequence[ServiceSettings] = SERVICES,
) -> tuple[str, ...]:
    """Return the names of the Services eligible for one API Group: published and asking for it.

    Args:
        services (Sequence[ServiceSettings]): The Services and their settings.
    """
    return tuple(
        service.name
        for service in services
        if service.publish_in_logic_interface and service.generate_api
    )


def validate_services(services: Sequence[ServiceSettings] = SERVICES) -> None:
    """Reject Services that break the fixed set, the API rule, or the identity rules.

    Args:
        services (Sequence[ServiceSettings]): The Services and their settings.
    """
    roles = sorted(service.role for service in services)
    if roles != ["entity", "storage"]:
        raise ConfigurationError(
            f"Logic carries exactly the fixed Entity and Storage Services, not {roles}."
        )
    unpublished = [
        service.name
        for service in services
        if service.generate_api and not service.publish_in_logic_interface
    ]
    if unpublished:
        raise ConfigurationError(
            f"API generation needs publication through the root Interface: {unpublished}."
        )
    validate_identities(service.name for service in services)
    validate_identities(service.directory for service in services)


def verify_publication(
    exports: Iterable[str], services: Sequence[ServiceSettings] = SERVICES
) -> None:
    """Require the root Interface to publish exactly the publication-enabled Services.

    Args:
        exports (Iterable[str]): The names the root Interface publishes.
        services (Sequence[ServiceSettings]): The Services and their settings.
    """
    validate_services(services)
    published = sorted(exports)
    expected = sorted(published_names(services))
    if published != expected:
        raise ConfigurationError(
            f"The root Interface must publish exactly the Services whose publication is "
            f"enabled {expected}, not {published}."
        )
