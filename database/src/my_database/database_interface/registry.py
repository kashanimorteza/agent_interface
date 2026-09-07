"""Instance discovery: the public identities of the configured Instances."""

from __future__ import annotations

from dataclasses import dataclass

from ..errors import UnknownInstanceError
from ..storage_adapter import Settings, load_settings


@dataclass(frozen=True)
class InstanceIdentity:
    """What a consumer may know about an Instance: no connection detail, no secret."""

    key: str
    name: str
    purpose: str
    engine: str


class InstanceRegistry:
    """The configured Instances and the default among them."""

    def __init__(self, settings: Settings | None = None) -> None:
        settings = settings or load_settings()
        self._instances = tuple(
            InstanceIdentity(key=i.key, name=i.name, purpose=i.purpose, engine=i.engine) for i in settings.instances.values()
        )
        self._default = settings.default
        if self._default not in settings.instances:
            raise UnknownInstanceError(
                f"the default Instance {self._default!r} is not configured; configured Instances: {', '.join(settings.instances)}"
            )

    @property
    def default(self) -> str:
        return self._default

    @property
    def instances(self) -> tuple[InstanceIdentity, ...]:
        return self._instances

    def get(self, key: str) -> InstanceIdentity:
        for identity in self._instances:
            if identity.key == key:
                return identity
        raise UnknownInstanceError(f"Instance {key!r} is not configured; configured Instances: {', '.join(i.key for i in self._instances)}")

    def __iter__(self):
        return iter(self._instances)

    def __len__(self) -> int:
        return len(self._instances)

    def __repr__(self) -> str:
        return f"InstanceRegistry(default={self._default!r}, instances={[i.key for i in self._instances]!r})"
