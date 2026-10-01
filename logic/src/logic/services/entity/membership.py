"""Child Service membership, learned only from Model's Entity Collection."""

from collections.abc import Iterable

from model.interface import entities

from logic.core.errors import ConfigurationError
from logic.services.entity.base_entity import BaseEntity


def ordered_children(
    children: Iterable[type[BaseEntity]],
) -> tuple[type[BaseEntity], ...]:
    """Return the Child Services in the Entity Collection's order, requiring exactly one per Entity.

    Args:
        children (Iterable[type[BaseEntity]]): The Child Services to present.
    """
    bound: dict[type, type[BaseEntity]] = {}
    repeated: list[str] = []
    for child in children:
        if child._entity in bound:
            repeated.append(child._entity.__name__)
        bound[child._entity] = child
    missing = [entity.__name__ for entity in entities if entity not in bound]
    extra = [
        child.__name__ for entity, child in bound.items() if entity not in entities
    ]
    if missing or extra or repeated:
        raise ConfigurationError(
            "Entity Service needs exactly one Child Service for every Entity of the Model "
            f"Entity Collection; missing {missing}, unexpected {extra}, repeated {repeated}."
        )
    return tuple(bound[entity] for entity in entities)
