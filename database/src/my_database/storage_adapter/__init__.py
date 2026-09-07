"""Storage Adapter — the layer that owns the connection to the Database Engine
and performs physical persistence operations.

Consumed only by Data Logic and Mapping and by the migration tooling.
"""

from .engine import SUPPORTED_ENGINES, make_engine
from .operations import Storage
from .settings import (
    DEFAULT_INSTANCE,
    DEFAULT_KEY_SECRET,
    InstanceSettings,
    Settings,
    credential_key,
    load_settings,
    project_root,
    resolve_path,
)

__all__ = [
    "DEFAULT_INSTANCE",
    "DEFAULT_KEY_SECRET",
    "SUPPORTED_ENGINES",
    "InstanceSettings",
    "Settings",
    "Storage",
    "credential_key",
    "load_settings",
    "make_engine",
    "project_root",
    "resolve_path",
]
