"""Declaration (public): immutable records of Entity and Field meaning."""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Final

from model.core._types import FieldType, is_valid_value, parse_field_type

__all__ = [
    "ABSENT",
    "Declaration",
    "FieldConstraints",
    "FieldDeclaration",
    "FieldType",
    "Relation",
    "Sensitivity",
    "ValueGeneration",
]


class ValueGeneration(StrEnum):
    auto_increment = "auto_increment"
    generated_identifier = "generated_identifier"


class Sensitivity(StrEnum):
    password = "password"
    sensitive = "sensitive"


class _Absent:
    __slots__ = ()

    def __repr__(self) -> str:
        return "ABSENT"


ABSENT: Final = _Absent()
"""The Default Value of a Field that declares none, distinct from an explicit null."""


def _require_name(label: str, value: object) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be a non-empty string")


def _require_tuple(label: str, value: object) -> None:
    if not isinstance(value, tuple):
        raise TypeError(f"{label} must be a tuple")


@dataclass(frozen=True, slots=True, kw_only=True)
class FieldConstraints:
    size: int | None = None

    def __post_init__(self) -> None:
        size = self.size
        if size is not None and (
            isinstance(size, bool) or not isinstance(size, int) or size < 1
        ):
            raise ValueError("A size constraint must be a positive length")


@dataclass(frozen=True, slots=True, kw_only=True)
class Relation:
    local_field: str
    target_entity: str
    target_field: str

    def __post_init__(self) -> None:
        _require_name("Relation local_field", self.local_field)
        _require_name("Relation target_entity", self.target_entity)
        _require_name("Relation target_field", self.target_field)


@dataclass(frozen=True, slots=True, kw_only=True)
class FieldDeclaration:
    name: str
    type: FieldType
    nullable: bool
    description: str | None = None
    default: object = ABSENT
    sensitivity: Sensitivity | None = None
    immutable: bool = False
    constraints: FieldConstraints = field(default_factory=FieldConstraints)
    value_generation: ValueGeneration | None = None

    def __post_init__(self) -> None:
        _require_name("Field name", self.name)
        object.__setattr__(self, "type", parse_field_type(self.type))
        label = f"Field {self.name!r}"
        if self.description is not None and not isinstance(self.description, str):
            raise TypeError(f"{label}: description must be a string or null")
        if not isinstance(self.nullable, bool) or not isinstance(self.immutable, bool):
            raise TypeError(f"{label}: nullable and immutable must be booleans")
        if self.sensitivity is not None and not isinstance(
            self.sensitivity, Sensitivity
        ):
            raise TypeError(f"{label}: unrecognized Sensitivity Marker")
        if not isinstance(self.constraints, FieldConstraints):
            raise TypeError(f"{label}: constraints must be FieldConstraints")
        size = self.constraints.size
        if size is not None and self.type is not FieldType.string:
            raise ValueError(f"{label}: a size applies only to a string Field")
        self._check_generation(label)
        self._check_default(label, size)

    def _check_generation(self, label: str) -> None:
        generation = self.value_generation
        if generation is None:
            return
        if not isinstance(generation, ValueGeneration):
            raise TypeError(f"{label}: unrecognized Value Generation")
        if self.default is not ABSENT:
            raise ValueError(f"{label}: a Default Value cannot coexist with generation")
        if generation is ValueGeneration.auto_increment:
            if self.type is not FieldType.integer:
                raise ValueError(f"{label}: Auto Increment requires an integer Field")
        elif self.type not in (FieldType.uuid, FieldType.string):
            raise ValueError(
                f"{label}: a Generated Identifier requires a uuid or string Field"
            )

    def _check_default(self, label: str, size: int | None) -> None:
        default = self.default
        if default is ABSENT:
            return
        if default is None:
            if not self.nullable:
                raise ValueError(f"{label}: a non-nullable Field has a null default")
            return
        if not is_valid_value(self.type, default):
            raise ValueError(f"{label}: the Default Value does not match its Type")
        if size is not None and isinstance(default, str) and len(default) > size:
            raise ValueError(f"{label}: the Default Value exceeds its size")


@dataclass(frozen=True, slots=True, kw_only=True)
class Declaration:
    name: str
    description: str
    fields: tuple[FieldDeclaration, ...]
    primary_key: str
    relations: tuple[Relation, ...] = ()
    unique_constraints: tuple[tuple[str, ...], ...] = ()
    indexes: tuple[tuple[str, ...], ...] = ()

    def __post_init__(self) -> None:
        _require_name("Entity name", self.name)
        label = f"Entity {self.name!r}"
        if not isinstance(self.description, str):
            raise TypeError(f"{label}: description must be a string")
        for member in ("fields", "relations", "unique_constraints", "indexes"):
            _require_tuple(f"{label}: {member}", getattr(self, member))
        if not all(isinstance(item, FieldDeclaration) for item in self.fields):
            raise TypeError(f"{label}: fields must be FieldDeclaration records")
        names = [item.name for item in self.fields]
        if len(set(names)) != len(names):
            raise ValueError(f"{label}: Field names must be unique")
        self._check_identity(label)
        self._check_relations(label, set(names))
        self._check_field_sets(label, "unique_constraints", set(names))
        self._check_field_sets(label, "indexes", set(names))

    def _check_identity(self, label: str) -> None:
        by_name = {item.name: item for item in self.fields}
        identity = by_name.get("id")
        if self.primary_key != "id" or identity is None:
            raise ValueError(f"{label}: the Primary Key must name the id Field")
        if identity.nullable or not identity.immutable:
            raise ValueError(f"{label}: id must be non-nullable and immutable")
        activity = by_name.get("is_active")
        if (
            activity is None
            or activity.type is not FieldType.boolean
            or activity.nullable
            or activity.immutable
        ):
            raise ValueError(
                f"{label}: is_active must be a non-nullable, mutable boolean"
            )

    def _check_relations(self, label: str, names: set[str]) -> None:
        if not all(isinstance(item, Relation) for item in self.relations):
            raise TypeError(f"{label}: relations must be Relation records")
        locals_ = [item.local_field for item in self.relations]
        if not set(locals_) <= names:
            raise ValueError(f"{label}: a Relation names an unknown local Field")
        if len(set(locals_)) != len(locals_):
            raise ValueError(f"{label}: a local Field has at most one Relation")

    def _check_field_sets(self, label: str, member: str, names: set[str]) -> None:
        entries: tuple[tuple[str, ...], ...] = getattr(self, member)
        for entry in entries:
            _require_tuple(f"{label}: {member} entry", entry)
            if not entry or not set(entry) <= names or len(set(entry)) != len(entry):
                raise ValueError(
                    f"{label}: each {member} entry must name known Fields once each"
                )
        if len(set(entries)) != len(entries):
            raise ValueError(f"{label}: {member} must not repeat an entry")
