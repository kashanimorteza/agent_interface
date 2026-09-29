"""Group eligibility: which Logic Services receive an API Group.

Logic's own Service settings are the only authority. API keeps no Service list of its own: the
caller supplies the settings read from Logic, and the eligible Services follow them exactly.
"""

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class ServiceSettings:
    """The settings Logic declares for one Service.

    Attributes:
        publish_in_logic_interface (bool): Whether Logic Interface publishes the Service.
        generate_api (bool): Whether the Service requests an API Group.
    """

    publish_in_logic_interface: bool
    generate_api: bool


def eligible_services(services: Mapping[str, ServiceSettings]) -> tuple[str, ...]:
    """Return the Services that receive an API Group, in the order given.

    Args:
        services (Mapping[str, ServiceSettings]): Logic's settings keyed by Service name.

    Returns:
        (tuple[str, ...]): Names of the Services with both settings enabled.

    Raises:
        ValueError: When a Service requests API generation while unpublished; the message
            names the Service.
    """
    for name, settings in services.items():
        if settings.generate_api and not settings.publish_in_logic_interface:
            raise ValueError(
                f"Service {name} requests API generation but is not published in Logic Interface"
            )
    return tuple(
        name
        for name, settings in services.items()
        if settings.publish_in_logic_interface and settings.generate_api
    )
