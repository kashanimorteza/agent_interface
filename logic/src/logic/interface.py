"""Logic Interface: one entry for every Service Interface of Logic."""

from logic.services.entity import interface as Entity
from logic.services.storage import interface as Storage

__all__ = ["Entity", "Storage"]
