"""Realization identities of Entity Service: Base Entity and every Child Service."""

import re
from collections.abc import Iterable
from typing import Final

from logic.core.errors import ConfigurationError
from logic.core.identity import validate_identities
from logic.services.entity.base_entity import BaseEntity

BASE_UNIT: Final = "base_entity"
BASE_STRUCTURE: Final = "BaseEntity"
CHILD_SUFFIX: Final = "Service"
CHILDREN_PACKAGE: Final = "logic.services.entity.entity"


def child_unit(entity_name: str) -> str:
    """Return the unit name of an Entity's Child Service: the Entity name in snake case."""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", entity_name).lower()


def child_structure(entity_name: str) -> str:
    """Return the public name of an Entity's Child Service: the Entity name and the suffix."""
    return f"{entity_name}{CHILD_SUFFIX}"


def verify_realization(children: Iterable[type[BaseEntity]]) -> None:
    """Require Base Entity and every Child to carry valid, unique, pattern-derived identities.

    Args:
        children (Iterable[type[BaseEntity]]): The Child Services Entity Service presents.
    """
    children = list(children)
    names = [child._entity.__name__ for child in children]
    validate_identities([BASE_UNIT, *map(child_unit, names)])
    validate_identities([BASE_STRUCTURE, *map(child_structure, names)])
    mismatches = [
        f"{child.__module__}.{child.__name__}"
        for child, name in zip(children, names, strict=True)
        if (child.__module__, child.__name__)
        != (f"{CHILDREN_PACKAGE}.{child_unit(name)}", child_structure(name))
    ]
    if (BaseEntity.__module__.rpartition(".")[2], BaseEntity.__name__) != (
        BASE_UNIT,
        BASE_STRUCTURE,
    ):
        mismatches.append(f"{BaseEntity.__module__}.{BaseEntity.__name__}")
    if mismatches:
        raise ConfigurationError(
            f"These realizations do not follow the configured patterns: {mismatches}."
        )
