"""What a consumer may know about the stored identities it can act on.

An identity here is a name and a purpose, and nothing that connects to anything.
It is derived from the settings this layer owns rather than kept as a second
catalogue beside them, so there is only ever one answer to what exists.
"""

from __future__ import annotations

from typing import Iterable, Iterator

from ..contract import InstanceDescription


class InstanceIdentity(InstanceDescription):
    """One stored identity, as a consumer sees it."""

    def __str__(self) -> str:
        return f"{self.name} ({self.key})"


class InstanceRegistry:
    """The published catalogue of stored identities and the default among them."""

    def __init__(self, described: Iterable[InstanceDescription], default: str) -> None:
        self._identities = {
            description.key: InstanceIdentity(
                key=description.key,
                name=description.name,
                purpose=description.purpose,
                engine=description.engine,
            )
            for description in described
        }
        self._default = default

    @property
    def default(self) -> InstanceIdentity:
        """The identity used when a caller names none."""

        return self._identities[self._default]

    def identities(self) -> tuple[InstanceIdentity, ...]:
        """Every identity a caller may select."""

        return tuple(self._identities.values())

    def get(self, key: str) -> InstanceIdentity:
        """One identity by key, refusing a key nobody declared."""

        if key not in self._identities:
            known = ", ".join(sorted(self._identities))
            raise KeyError(f"no Instance named {key!r}; the declared ones are {known}")
        return self._identities[key]

    def __iter__(self) -> Iterator[InstanceIdentity]:
        return iter(self._identities.values())

    def __contains__(self, key: object) -> bool:
        return key in self._identities

    def __len__(self) -> int:
        return len(self._identities)

    def __repr__(self) -> str:
        return f"InstanceRegistry({', '.join(sorted(self._identities))}; default={self._default})"


__all__ = ["InstanceIdentity", "InstanceRegistry"]
