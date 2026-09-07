"""The defined Instances and the default, derived from the runtime settings."""

from __future__ import annotations

from collections.abc import Iterator

from ..errors import UnknownInstance
from ..runtime import DatabaseSettings, InstanceSettings

SUPPORTED_ENGINES = ("SQLite", "PostgreSQL", "MySQL")


class InstanceCollection:
    """The defined Instances, with exactly one default.

    The number of Instances is derived from the collection.
    """

    def __init__(self, settings: DatabaseSettings) -> None:
        self._settings = settings
        for key, raw in settings.instances.items():
            if raw.engine not in SUPPORTED_ENGINES:
                raise UnknownInstance(f"instance {key!r} uses unsupported engine {raw.engine!r}")

    @property
    def default_key(self) -> str:
        return self._settings.default_instance

    def resolve_key(self, key: str | None) -> str:
        """The key to use: the given one when defined, else the default."""
        if key is None:
            return self._settings.default_instance
        if key not in self._settings.instances:
            raise UnknownInstance(f"unknown Instance {key!r}; defined: {sorted(self._settings.instances)}")
        return key

    def settings_for(self, key: str | None = None) -> InstanceSettings:
        return self._settings.instances[self.resolve_key(key)]

    def __iter__(self) -> Iterator[InstanceSettings]:
        return iter(self._settings.instances.values())

    def __len__(self) -> int:
        return len(self._settings.instances)

    def __contains__(self, key: object) -> bool:
        return key in self._settings.instances
