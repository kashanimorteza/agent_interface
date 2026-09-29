"""Entity Group: Entity Service published as one API Group.

There is one Group for Entity Service and every Entity Child Service is a resource inside it, so
no Entity has a Group of its own.
"""

from fastapi import APIRouter

from trading_assistant_api.core.endpoints import Endpoint, segment
from trading_assistant_api.groups.entity import adapter
from trading_assistant_api.groups.entity.endpoints import GROUP, endpoints
from trading_assistant_api.groups.entity.router import create_router
from trading_assistant_api.groups.entity.shapes import shape_of

SERVICE = "Entity"


def resources() -> tuple[str, ...]:
    """Return the resources of the Group: one per Entity Child Service.

    Returns:
        (tuple[str, ...]): Route segments of the Child Services Entity Service publishes.
    """
    return tuple(segment(child) for child in adapter.children())


def build(generated: list[Endpoint]) -> APIRouter:
    """Serve the Group's Endpoints through its Router.

    Args:
        generated (list[Endpoint]): The Group's validated Endpoints.

    Returns:
        (APIRouter): The Group's Router.
    """
    return create_router(GROUP, generated, shape_of)


__all__ = ["GROUP", "SERVICE", "build", "endpoints", "resources"]
