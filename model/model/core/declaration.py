"""The public Declaration contract: the complete, read-only logical meaning of an Entity.

A Declaration holds no runtime behaviour. Its structural rules are checked when it is created, and
an invalid or contradictory Declaration fails instead of being repaired.
"""

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from model.core._types import PYTHON_TYPES, FieldType


class ValueGeneration(StrEnum):
    """The ways a Field value can be supplied automatically."""

    auto_increment = "auto_increment"
    generated_identifier = "generated_identifier"


class Sensitivity(StrEnum):
    """The recognized Sensitivity Markers. A marker records meaning and changes no value."""

    password = "password"
    sensitive = "sensitive"


@dataclass(frozen=True, slots=True)
class FieldConstraints:
    """The value constraints of one Field."""

    size: int | None = None


@dataclass(frozen=True, slots=True)
class FieldDeclaration:
    """The complete public record of one Field.

    ``has_default`` separates an absent Default Value from an explicit null default.
    """

    name: str
    type: FieldType
    nullable: bool
    description: str | None = None
    has_default: bool = False
    default: Any = None
    sensitivity: Sensitivity | None = None
    immutable: bool = False
    constraints: FieldConstraints = FieldConstraints()
    value_generation: ValueGeneration | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.type, FieldType):
            raise TypeError(f"Field {self.name}: type must be a FieldType")
        if self.sensitivity is not None and not isinstance(self.sensitivity, Sensitivity):
            raise TypeError(f"Field {self.name}: unrecognized Sensitivity Marker")
        if self.value_generation is not None and not isinstance(
            self.value_generation, ValueGeneration
        ):
            raise TypeError(f"Field {self.name}: unrecognized Value Generation")
        if not self.has_default and self.default is not None:
            raise ValueError(f"Field {self.name}: a default is given but has_default is false")
        if self.has_default and self.value_generation is not None:
            raise ValueError(f"Field {self.name}: a Default Value and Value Generation conflict")
        if self.has_default:
            self._check_default()
        if self.value_generation is ValueGeneration.auto_increment and (
            self.type is not FieldType.integer
        ):
            raise ValueError(f"Field {self.name}: auto_increment requires the integer Type")
        if self.value_generation is ValueGeneration.generated_identifier and (
            self.type not in (FieldType.uuid, FieldType.string)
        ):
            raise ValueError(f"Field {self.name}: generated_identifier requires uuid or string")
        size = self.constraints.size
        if size is not None and (
            self.type is not FieldType.string or isinstance(size, bool) or size < 1
        ):
            raise ValueError(f"Field {self.name}: size is a positive length of a string Field")

    def _check_default(self) -> None:
        if self.default is None:
            if not self.nullable:
                raise ValueError(f"Field {self.name}: a non-nullable Field has a null default")
            return
        expected = PYTHON_TYPES[self.type]
        if type(self.default) is bool and expected is not bool:
            raise ValueError(f"Field {self.name}: the default does not match the Type")
        if not isinstance(self.default, expected):
            raise ValueError(f"Field {self.name}: the default does not match the Type")


@dataclass(frozen=True, slots=True)
class Relation:
    """A connection from one local Field to a target Entity and target Field by logical name."""

    local_field: str
    target_entity: str
    target_field: str


@dataclass(frozen=True, slots=True)
class UniqueConstraint:
    """A Field, or ordered combination of Fields, that must be unique."""

    fields: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Index:
    """An access intention for a Field or ordered combination of Fields."""

    fields: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Declaration:
    """The complete public record of one Entity: its meaning, Fields, and Entity Metadata."""

    name: str
    description: str | None
    fields: tuple[FieldDeclaration, ...]
    primary_key: str
    relations: tuple[Relation, ...] = ()
    unique_constraints: tuple[UniqueConstraint, ...] = ()
    indexes: tuple[Index, ...] = ()

    def __post_init__(self) -> None:
        for collection in (self.fields, self.relations, self.unique_constraints, self.indexes):
            if not isinstance(collection, tuple):
                raise TypeError(f"Entity {self.name}: collections must be tuples")
        by_name = {field.name: field for field in self.fields}
        if len(by_name) != len(self.fields):
            raise ValueError(f"Entity {self.name}: a Field name is repeated")
        self._check_structure(by_name)
        self._check_metadata(by_name)

    def _check_structure(self, by_name: dict[str, FieldDeclaration]) -> None:
        identity = by_name.get(self.primary_key)
        if identity is None or self.primary_key != "id":
            raise ValueError(f"Entity {self.name}: the Primary Key must name the id Field")
        if identity.nullable or not identity.immutable:
            raise ValueError(f"Entity {self.name}: id must be non-nullable and immutable")
        activity = by_name.get("is_active")
        if (
            activity is None
            or activity.type is not FieldType.boolean
            or activity.nullable
            or activity.immutable
        ):
            raise ValueError(
                f"Entity {self.name}: is_active must be a non-nullable mutable boolean"
            )

    def _check_metadata(self, by_name: dict[str, FieldDeclaration]) -> None:
        local_fields = [relation.local_field for relation in self.relations]
        if any(name not in by_name for name in local_fields):
            raise ValueError(f"Entity {self.name}: a Relation names an unknown local Field")
        if len(set(local_fields)) != len(local_fields):
            raise ValueError(f"Entity {self.name}: a Relation is repeated for one local Field")
        for kind, entries in (
            ("Uniqueness Constraint", self.unique_constraints),
            ("Index", self.indexes),
        ):
            seen: set[tuple[str, ...]] = set()
            for entry in entries:
                names = entry.fields
                if not isinstance(names, tuple) or not names:
                    raise ValueError(f"Entity {self.name}: a {kind} needs a tuple of Fields")
                if any(name not in by_name for name in names):
                    raise ValueError(f"Entity {self.name}: a {kind} names an unknown Field")
                if len(set(names)) != len(names):
                    raise ValueError(f"Entity {self.name}: a {kind} repeats a Field")
                if names in seen:
                    raise ValueError(f"Entity {self.name}: a {kind} is duplicated")
                seen.add(names)
