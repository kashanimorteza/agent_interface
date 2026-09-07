"""my_backend: the application layer of the Trading Assistant.

Its external interface is the HTTP API the server publishes. In-process, the
package exposes ``create_app`` to build that API and ``resolve_settings`` to
read the Backend section of the runtime configuration. The Data Access,
Logic, and API layers are internal and are never imported by consumers.
"""

from .api import create_app
from .runtime import BackendSettings, ConfigurationError, resolve_settings

__all__ = ["create_app", "resolve_settings", "BackendSettings", "ConfigurationError"]
