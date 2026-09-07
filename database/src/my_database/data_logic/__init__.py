"""Data Logic and Mapping — the layer that implements the generic Model
operations and resolves the persistence mapping and enforcement of the shared
Models, their relationships, rules, credential modes, and initial data.

Consumed only by the Database Interface layer and by the migration tooling.
"""

from . import credentials, seeding
from .mapping import PERSISTENCE, TABLES, Mapped, Persistence, mapped, metadata

__all__ = ["PERSISTENCE", "TABLES", "Mapped", "Persistence", "credentials", "mapped", "metadata", "seeding"]
from .operations import Operations  # noqa: E402

__all__.append("Operations")
