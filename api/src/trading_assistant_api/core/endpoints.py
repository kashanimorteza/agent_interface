"""Endpoint descriptors and the validation of Group identities and final routes.

Validation runs before the boundary is realized. An invalid identity or a colliding route stops
generation with an error that names it; nothing is ever renamed, suffixed, or numbered to make a
value fit.
"""

import re
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass

IDENTITY = re.compile(r"[a-z][a-z0-9_]*")
VERSION = re.compile(r"v[0-9]+")


class InvalidRoutes(ValueError):
    """A Group identity, route segment, or final route is invalid or collides."""


@dataclass(frozen=True)
class Endpoint:
    """The public HTTP representation of one API-enabled callable Action.

    Attributes:
        group (str): Identity of the Group that owns the Endpoint.
        identity (str): Action identity, `<Child Service>.<action>`.
        method (str): Explicit HTTP method.
        path (str): Route below the version prefix, including the Group prefix.
    """

    group: str
    identity: str
    method: str
    path: str


def segment(name: str) -> str:
    """Normalize a Service or Child Service name to a route segment.

    Args:
        name (str): CamelCase name, optionally ending in `Service`.

    Returns:
        (str): The snake_case segment without the `Service` suffix.
    """
    name = name.removesuffix("Service")
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name).lower()


def validate_endpoints(version: str, endpoints: Iterable[Endpoint]) -> None:
    """Validate Group identities and the final method-and-route combinations.

    Args:
        version (str): Version prefix every route is served under.
        endpoints (Iterable[Endpoint]): Every Endpoint of every Group.

    Raises:
        InvalidRoutes: When the version, a Group identity, a route segment, or a final
            method-and-route combination is invalid or duplicated; the message names each.
    """
    problems: list[str] = []
    if not VERSION.fullmatch(version):
        problems.append(f"invalid version {version!r}")
    seen: dict[tuple[str, str], list[str]] = defaultdict(list)
    for endpoint in endpoints:
        if not IDENTITY.fullmatch(endpoint.group):
            problems.append(f"invalid Group identity {endpoint.group!r}")
        parts = endpoint.path.split("/")
        if parts[0] or not all(IDENTITY.fullmatch(part) for part in parts[1:]):
            problems.append(f"invalid route {endpoint.path!r} of {endpoint.identity}")
        seen[(endpoint.method, f"/{version}{endpoint.path}")].append(endpoint.identity)
    for (method, path), identities in seen.items():
        if len(identities) > 1:
            problems.append(f"{method} {path} is used by " + " and ".join(identities))
    if problems:
        raise InvalidRoutes("; ".join(dict.fromkeys(problems)))
