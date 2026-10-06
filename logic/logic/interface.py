"""The Logic Interface: every Service Interface, under its Service name."""

from logic.services.entity import interface as Entity
from logic.services.storage import interface as Storage

__all__ = ["Entity", "Storage"]
