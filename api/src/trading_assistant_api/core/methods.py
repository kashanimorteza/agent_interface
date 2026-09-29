"""Endpoint methods: the explicit HTTP method of every Endpoint.

Neither Target nor API Preferences names a method; API Preferences leave it to the selected
realization. A Group therefore declares an explicit table, and a method is looked up in it by the
kind of Action and never derived from an Action's name. An Action the table does not cover is not
generated: resolution refuses it with an error that names it.
"""

from collections.abc import Iterable, Mapping

METHODS = frozenset({"GET", "POST", "PUT", "PATCH", "DELETE"})


class UnresolvedMethod(ValueError):
    """An Action has no declared method, so its Endpoint cannot be generated."""


def resolve_methods(
    identities: Iterable[str], declared: Mapping[str, str]
) -> dict[str, str]:
    """Return the declared method of every Endpoint.

    Args:
        identities (Iterable[str]): Action identities, `<Child Service>.<action>`.
        declared (Mapping[str, str]): The Group's explicit method for each kind of Action.

    Returns:
        (dict[str, str]): The method of each identity.

    Raises:
        UnresolvedMethod: When an Action has no declared method or a declared method is not an
            HTTP method; the message names every such Endpoint.
    """
    methods: dict[str, str] = {}
    unresolved: list[str] = []
    for identity in identities:
        method = declared.get(identity.rpartition(".")[2])
        if method in METHODS:
            methods[identity] = method
        else:
            unresolved.append(identity)
    if unresolved:
        raise UnresolvedMethod("No declared HTTP method for " + ", ".join(unresolved))
    return methods
