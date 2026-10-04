"""Logic Interface: every Service's own Interface, published under the Service's configured name."""

from logic.services.entity import interface as Entity
from logic.services.storage import interface as Storage

__all__ = [
    "Entity",
    "Storage",
]
