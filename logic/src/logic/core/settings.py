"""Declared Service settings and their validation."""

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field

from logic.core.errors import ConfigurationError
from logic.core.identifiers import check_identifiers


@dataclass(frozen=True, slots=True)
class ServiceSettings:
    """The declared settings of one Service.

    Attributes:
        role: Fixed role of the Service ("entity", "storage", or an additional Service's own role).
        name: Configured Service name under which Logic Interface publishes it.
        directory: Configured Service directory.
        publish_in_logic_interface: Whether Logic Interface publishes the Service Interface.
        generate_api: Whether an API Group is requested; valid only when published.
        action_generate_api: Action-level API-generation overrides by Action identity.
        action_names: Action-name overrides by stable Operation identity.
    """

    role: str
    name: str
    directory: str
    publish_in_logic_interface: bool
    generate_api: bool
    action_generate_api: Mapping[str, bool] = field(default_factory=dict)
    action_names: Mapping[str, str] = field(default_factory=dict)


ENTITY = ServiceSettings("entity", "Entity", "entity", True, True)
STORAGE = ServiceSettings("storage", "Storage", "storage", False, False)
SERVICES = (ENTITY, STORAGE)


def validate_services(
    services: Iterable[ServiceSettings],
) -> tuple[ServiceSettings, ...]:
    """Validate Service identities, the fixed Services, and API eligibility.

    Args:
        services (Iterable[ServiceSettings]): Declared Services.

    Returns:
        (tuple[ServiceSettings, ...]): The validated Services.
    """
    declared = tuple(services)
    roles = {service.role for service in declared}
    for fixed in ("entity", "storage"):
        if fixed not in roles:
            raise ConfigurationError(f"The fixed {fixed} Service cannot be removed")
    check_identifiers((service.name for service in declared), "Service name")
    check_identifiers((service.directory for service in declared), "Service directory")
    for service in declared:
        if service.generate_api and not service.publish_in_logic_interface:
            raise ConfigurationError(
                f"Service '{service.name}' requests API generation but is not published"
            )
    return declared


def published(services: Iterable[ServiceSettings]) -> tuple[ServiceSettings, ...]:
    """Return the Services whose Interface Logic Interface publishes.

    Args:
        services (Iterable[ServiceSettings]): Declared Services.

    Returns:
        (tuple[ServiceSettings, ...]): Publication-enabled Services, in order.
    """
    return tuple(service for service in services if service.publish_in_logic_interface)


def api_eligible(services: Iterable[ServiceSettings]) -> tuple[ServiceSettings, ...]:
    """Return the Services eligible for an API Group: published and requesting generation.

    Args:
        services (Iterable[ServiceSettings]): Declared Services.

    Returns:
        (tuple[ServiceSettings, ...]): Eligible Services, in order.
    """
    return tuple(s for s in published(services) if s.generate_api)


def api_actions(
    service: ServiceSettings, callable_actions: Iterable[str]
) -> tuple[str, ...]:
    """Return the Actions of an eligible Service that API may expose.

    Args:
        service (ServiceSettings): Service whose Actions are listed.
        callable_actions (Iterable[str]): Action identities the Service publishes.

    Returns:
        (tuple[str, ...]): Actions enabled by default and not explicitly excluded; empty for an ineligible Service.
    """
    actions = tuple(callable_actions)
    unknown = sorted(set(service.action_generate_api) - set(actions))
    if unknown:
        raise ConfigurationError(
            f"Service '{service.name}' overrides unknown Actions: {', '.join(unknown)}"
        )
    if not api_eligible([service]):
        return ()
    return tuple(a for a in actions if service.action_generate_api.get(a, True))


validate_services(SERVICES)
