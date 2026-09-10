from __future__ import annotations

from ._gateway import BoundDatabase, Database
from ._registry import InstanceIdentity, default_instance, list_instances
from ._seed import seed_all as seed_initial_data

gateway = Database()

__all__ = [
    "Database",
    "BoundDatabase",
    "gateway",
    "InstanceIdentity",
    "list_instances",
    "default_instance",
    "seed_initial_data",
]
