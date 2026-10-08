"""Interface: Logic's outward surface, one entry for every Service."""

from logic.services.entity import interface as Entity
from logic.services.storage import interface as Storage

__all__ = [
    "Entity",
    "Storage",
]
