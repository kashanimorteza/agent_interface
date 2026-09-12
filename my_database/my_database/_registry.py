"""The public Instance Registry: selectable Instance identities and the
default, built from the validated runtime Instance catalogue. Exposes no
connection object and no secret value.
"""

from __future__ import annotations

from dataclasses import dataclass

from my_database._config import load_runtime_configuration
from my_database._errors import UnknownInstanceError


@dataclass(frozen=True)
class InstanceIdentity:
    key: str
    name: str
    purpose: str


class InstanceRegistry:
    def list(self) -> list[InstanceIdentity]:
        config = load_runtime_configuration()
        return [
            InstanceIdentity(key=key, name=entry["name"], purpose=entry["purpose"])
            for key, entry in config["instances"].items()
        ]

    @property
    def default(self) -> InstanceIdentity:
        config = load_runtime_configuration()
        default_key = config["default_instance"]
        for identity in self.list():
            if identity.key == default_key:
                return identity
        raise UnknownInstanceError(
            f"Configured default_instance {default_key!r} is not a configured Instance."
        )

    def resolve(self, instance: str | None) -> InstanceIdentity:
        key = instance if instance is not None else self.default.key
        for identity in self.list():
            if identity.key == key:
                return identity
        raise UnknownInstanceError(f"{key!r} is not a configured Database Instance.")


instances = InstanceRegistry()
