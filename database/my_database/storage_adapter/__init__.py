"""Storage Adapter — the engine, the Instances, and the settings this layer owns.

The lowest of the three responsibilities inside this package. It knows which
engine an Instance is reached through and how to reach it; it knows nothing
about domain definitions. Only the mapping layer above it uses this, and no
consumer sees any of it.
"""

from .configuration import (
    Configuration,
    ConfigurationError,
    EngineProfile,
    InstanceSetting,
    data_directory,
    layer_root,
    load,
    settings_file,
    validate,
)
from .connections import Connection, Connections, storage_location
from .secrets import ENCRYPTION_KEY, MissingSecret, declared_names, require, resolve

__all__ = [
    "ENCRYPTION_KEY",
    "Configuration",
    "ConfigurationError",
    "Connection",
    "Connections",
    "EngineProfile",
    "InstanceSetting",
    "MissingSecret",
    "data_directory",
    "declared_names",
    "layer_root",
    "load",
    "require",
    "resolve",
    "settings_file",
    "storage_location",
    "validate",
]
