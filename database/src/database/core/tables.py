"""Coordinate Create Tables for an Instance."""

from collections.abc import Sequence
from typing import Any

from database.core import structure


def create_tables(instance: Any, entities: Sequence[Any] | None = None) -> None:
    """Create or migrate the stored structure of Entities on an Instance.

    Args:
        instance (Any): Instance implementation to prepare.
        entities (Sequence[Any], optional): Entities to realize; defaults to every Model Entity.
    """
    instance.create_tables(structure.entity_classes() if entities is None else entities)
