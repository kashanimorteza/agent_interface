"""The public Database Instance Registry."""

from __future__ import annotations

from dataclasses import dataclass

from .exceptions import UnknownDatabaseInstance
from .runtime_config import RuntimeConfig, load_runtime_config


@dataclass(frozen=True, slots=True)
class InstanceInfo:
    """One Database Instance's publishable identity. Never carries a connection or secret."""

    key: str
    name: str
    purpose: str
    is_default: bool


class InstanceRegistry:
    """Publishes every configured Database Instance's identity and the default selection."""

    def __init__(self, config: RuntimeConfig | None = None) -> None:
        self._config = config or load_runtime_config()

    def list_instances(self) -> tuple[InstanceInfo, ...]:
        return tuple(
            InstanceInfo(
                key=instance.key,
                name=instance.name,
                purpose=instance.purpose,
                is_default=(instance.key == self._config.default_instance),
            )
            for instance in self._config.instances.values()
        )

    @property
    def default(self) -> InstanceInfo:
        return self.get(self._config.default_instance)

    def get(self, key: str) -> InstanceInfo:
        if key not in self._config.instances:
            raise UnknownDatabaseInstance(f"No configured Database Instance named {key!r}")
        instance = self._config.instances[key]
        return InstanceInfo(
            key=instance.key,
            name=instance.name,
            purpose=instance.purpose,
            is_default=(instance.key == self._config.default_instance),
        )
