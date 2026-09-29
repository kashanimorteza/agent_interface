"""Interface: the single root through which every consumer reaches Logic.

It publishes each Service Interface unchanged under that Service's configured name.
"""

from logic.services.entity import interface as Entity
from logic.services.storage import interface as Storage

__all__ = ["Entity", "Storage"]
