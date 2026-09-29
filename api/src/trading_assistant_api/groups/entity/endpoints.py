"""Entity Group Endpoints: the explicit method and route of every API-enabled Action.

Entity Service is one Group and each Entity Child Service is a resource of it. Every callable
Action of a Child Service becomes one Endpoint at `/entity/<resource>/<action>`, except an Action
Entity Service disables for API generation (none today).
"""

from trading_assistant_api.core.endpoints import Endpoint, segment
from trading_assistant_api.core.methods import resolve_methods
from trading_assistant_api.groups.entity import adapter

GROUP = "entity"

# The realization's explicit choice for each kind of Entity Action. Reads are GET and use the
# query string; a request that carries a whole record is POST (create) or PUT (replace); an
# Action that changes one record's state is POST; removal is DELETE.
METHODS = {
    "add": "POST",
    "update": "PUT",
    "list": "GET",
    "get_by_id": "GET",
    "count": "GET",
    "sum": "GET",
    "min": "GET",
    "max": "GET",
    "enable": "POST",
    "disable": "POST",
    "delete": "DELETE",
    "truncate": "DELETE",
}


def endpoints(
    declared: dict[str, str] = METHODS,
    disabled: frozenset[str] = adapter.DISABLED_ACTIONS,
) -> list[Endpoint]:
    """Return one Endpoint for every API-enabled callable Action of Entity Service.

    Args:
        declared (dict[str, str]): Explicit method for each kind of Action.
        disabled (frozenset[str]): Action identities that disable API generation.

    Returns:
        (list[Endpoint]): The Endpoints in Action order.

    Raises:
        UnresolvedMethod: When an Action has no declared method; the message names it.
    """
    identities = list(adapter.actions(disabled))
    methods = resolve_methods(identities, declared)
    return [
        Endpoint(
            GROUP,
            identity,
            methods[identity],
            f"/{GROUP}/{segment(child)}/{action}",
        )
        for identity in identities
        for child, _, action in [identity.partition(".")]
    ]
