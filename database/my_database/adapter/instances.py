"""Instance identities and the rules for selecting one.

An omitted selection uses the declared default. A selection naming an
Instance that was never declared is refused; it is never answered with the
default or with any other Instance. The number of Instances is derived from
the declared collection.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any

from ..config import DatabaseSettings, InstanceProfile
from ..errors import UnknownInstance


@dataclass(frozen=True)
class Instance:
    """One selectable database identity.

    It carries what a consumer needs to choose an Instance and nothing that
    would let it connect: no connection, no storage location, no secret.
    """

    key: str
    name: str
    purpose: str
    engine: str
    database: str
    is_default: bool


class InstanceCollection:
    """Every declared Instance, with exactly one default."""

    def __init__(self, settings: DatabaseSettings) -> None:
        self._settings = settings
        self._identities = {
            key: Instance(
                key=key,
                name=profile.name,
                purpose=profile.purpose,
                engine=profile.engine,
                database=profile.database,
                is_default=(key == settings.default_instance),
            )
            for key, profile in settings.instances.items()
        }

    @property
    def default(self) -> Instance:
        return self._identities[self._settings.default_instance]

    def resolve_key(self, selection: Any = None) -> str:
        """The key to act on: the declared one selected, else the default.

        ``selection`` may be omitted, an Instance identity, or a key.
        """
        if selection is None:
            return self._settings.default_instance
        key = selection.key if isinstance(selection, Instance) else selection
        if not isinstance(key, str) or key not in self._identities:
            raise UnknownInstance(
                f"{key!r} is not a declared Instance; declared: {sorted(self._identities)}"
            )
        return key

    def get(self, selection: Any = None) -> Instance:
        return self._identities[self.resolve_key(selection)]

    def profile(self, selection: Any = None) -> InstanceProfile:
        return self._settings.instances[self.resolve_key(selection)]

    def __iter__(self) -> Iterator[Instance]:
        return iter(self._identities.values())

    def __len__(self) -> int:
        return len(self._identities)

    def __contains__(self, selection: object) -> bool:
        key = selection.key if isinstance(selection, Instance) else selection
        return key in self._identities
