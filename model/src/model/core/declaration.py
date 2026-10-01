"""The public, read-only record of what an Entity and each of its Fields mean."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any


def _no_constraints() -> Mapping[str, Any]:
    return MappingProxyType({})


@dataclass(frozen=True)
class Relation:
    """Connects one local Field to a target Entity and target Field by logical name."""

    local_field: str
    target_entity: str
    target_field: str


@dataclass(frozen=True)
class FieldDeclaration:
    """The complete value contract of one Field."""

    name: str
    description: str | None
    type: str
    nullable: bool
    has_default: bool = False
    default: Any = None
    sensitivity: str | None = None
    immutable: bool = False
    constraints: Mapping[str, Any] = field(default_factory=_no_constraints)
    value_generation: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "constraints", MappingProxyType(dict(self.constraints))
        )


@dataclass(frozen=True)
class Declaration:
    """The complete structured record of one Entity."""

    name: str
    description: str
    fields: tuple[FieldDeclaration, ...]
    primary_key: str
    relations: tuple[Relation, ...]
    unique_constraints: tuple[tuple[str, ...], ...]
    indexes: tuple[tuple[str, ...], ...]
