"""Model's public Entities and Declarations, reached through Model's boundary."""

from functools import cache
from typing import Any

import model
from sqlmodel import SQLModel


@cache
def entity_classes() -> dict[str, type[SQLModel]]:
    """Every public Entity class, keyed by its public identity (its class name)."""
    return {name: getattr(model, name) for name in model.__all__}


def declaration_of(entity: type[SQLModel]) -> Any:
    """The complete public Declaration of one Entity class."""
    return getattr(entity, "Declaration")  # noqa: B009


@cache
def declarations() -> dict[str, Any]:
    """The complete public Declaration of every public Entity, by identity."""
    return {
        identity: declaration_of(entity)
        for identity, entity in entity_classes().items()
    }


def identity_of(entity: type[SQLModel]) -> str | None:
    """The public identity of an Entity class, or None when it is not public."""
    for identity, candidate in entity_classes().items():
        if candidate is entity:
            return identity
    return None
