"""The public Declaration contract: the structured meaning of Entities and Fields."""

from dataclasses import dataclass
from enum import Enum, StrEnum
from typing import Any, Final

from model.core._types import conforms


class FieldType(StrEnum):
    """The closed set of Field Types."""

    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    DECIMAL = "decimal"
    BOOLEAN = "boolean"
    DATETIME = "datetime"
    DATE = "date"
    TIME = "time"
    UUID = "uuid"


class ValueGeneration(StrEnum):
    """The declared ways a Field value is supplied automatically."""

    AUTO_INCREMENT = "auto_increment"
    GENERATED_IDENTIFIER = "generated_identifier"


class Sensitivity(StrEnum):
    """The recognized Sensitivity Markers."""

    PASSWORD = "password"
    SENSITIVE = "sensitive"


class NoDefault(Enum):
    """The type of NO_DEFAULT, which marks a Field without a Default Value."""

    NO_DEFAULT = "NO_DEFAULT"

    def __repr__(self) -> str:
        return "NO_DEFAULT"


NO_DEFAULT: Final = NoDefault.NO_DEFAULT
"""Marks the absence of a Default Value, distinct from an explicit null default."""

IDENTITY: Final = "id"
"""The name of the mandatory Identity Field."""

ACTIVITY: Final = "is_active"
"""The name of the mandatory Activity Field."""


class DeclarationError(ValueError):
    """Raised when a Declaration is invalid or contradictory."""

    def __init__(self, subject: str, problems: list[str]) -> None:
        self.subject = subject
        self.problems = tuple(problems)
        super().__init__(f"Invalid declaration of {subject}: " + "; ".join(problems))


def _require_tuple(problems: list[str], name: str, value: object) -> None:
    if not isinstance(value, tuple):
        problems.append(f"{name} must be a tuple")


@dataclass(frozen=True, slots=True, kw_only=True)
class FieldConstraints:
    """Value constraints of one Field."""

    size: int | None = None

    def __post_init__(self) -> None:
        if self.size is not None and (type(self.size) is not int or self.size <= 0):
            raise DeclarationError(
                "field constraints", ["size must be a positive integer"]
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class FieldDeclaration:
    """The complete public record of one Field."""

    name: str
    type: FieldType
    nullable: bool
    description: str | None = None
    default: Any = NO_DEFAULT
    sensitivity: Sensitivity | None = None
    immutable: bool = False
    constraints: FieldConstraints = FieldConstraints()
    value_generation: ValueGeneration | None = None

    def __post_init__(self) -> None:
        problems: list[str] = []
        if not isinstance(self.name, str) or not self.name:
            problems.append("name must be a non-empty string")
        if not isinstance(self.type, FieldType):
            problems.append(f"unknown Field Type {self.type!r}")
        if not isinstance(self.nullable, bool):
            problems.append("nullable must be a boolean")
        if self.description is not None and not isinstance(self.description, str):
            problems.append("description must be a string or None")
        if self.sensitivity is not None and not isinstance(
            self.sensitivity, Sensitivity
        ):
            problems.append(f"unknown Sensitivity Marker {self.sensitivity!r}")
        if not isinstance(self.immutable, bool):
            problems.append("immutable must be a boolean")
        if not isinstance(self.constraints, FieldConstraints):
            problems.append("constraints must be a FieldConstraints")
        if self.value_generation is not None and not isinstance(
            self.value_generation, ValueGeneration
        ):
            problems.append(f"unknown Value Generation {self.value_generation!r}")
        if problems:
            raise DeclarationError(f"field {self.name!r}", problems)

        if self.constraints.size is not None and self.type is not FieldType.STRING:
            problems.append("a size constraint applies only to a string Field")
        if self.value_generation is ValueGeneration.AUTO_INCREMENT and (
            self.type is not FieldType.INTEGER
        ):
            problems.append("auto_increment requires an integer Field")
        if self.value_generation is ValueGeneration.GENERATED_IDENTIFIER and (
            self.type not in (FieldType.UUID, FieldType.STRING)
        ):
            problems.append("generated_identifier requires a uuid or string Field")
        if self.default is not NO_DEFAULT:
            if self.value_generation is not None:
                problems.append("a Default Value cannot coexist with Value Generation")
            if self.default is None:
                if not self.nullable:
                    problems.append("a null default requires a nullable Field")
            elif not conforms(self.type, self.default):
                problems.append(f"the default does not match the {self.type} Type")
            elif (
                self.constraints.size is not None
                and len(self.default) > self.constraints.size
            ):
                problems.append("the default exceeds the size constraint")
        if problems:
            raise DeclarationError(f"field {self.name!r}", problems)


@dataclass(frozen=True, slots=True)
class Relation:
    """Connects one local Field to a target Entity and target Field by logical name."""

    local_field: str
    target_entity: str
    target_field: str


@dataclass(frozen=True, slots=True)
class UniquenessConstraint:
    """Requires one Field or an ordered combination of Fields to be unique."""

    fields: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Index:
    """Records an access intention for one Field or an ordered combination of Fields."""

    fields: tuple[str, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class Declaration:
    """The complete public record of one Entity."""

    name: str
    description: str
    fields: tuple[FieldDeclaration, ...]
    primary_key: str = IDENTITY
    relations: tuple[Relation, ...] = ()
    unique_constraints: tuple[UniquenessConstraint, ...] = ()
    indexes: tuple[Index, ...] = ()

    def __post_init__(self) -> None:
        problems: list[str] = []
        if not isinstance(self.name, str) or not self.name:
            problems.append("name must be a non-empty string")
        if not isinstance(self.description, str):
            problems.append("description must be a string")
        for member in ("fields", "relations", "unique_constraints", "indexes"):
            _require_tuple(problems, member, getattr(self, member))
        if problems:
            raise DeclarationError(f"entity {self.name!r}", problems)

        names = [field.name for field in self.fields]
        by_name = {field.name: field for field in self.fields}
        for name in sorted({name for name in names if names.count(name) > 1}):
            problems.append(f"Field {name!r} is declared more than once")

        if self.primary_key != IDENTITY:
            problems.append(f"the Primary Key must name {IDENTITY!r}")
        identity = by_name.get(IDENTITY)
        if identity is None:
            problems.append(f"the Identity Field {IDENTITY!r} is missing")
        elif identity.nullable or not identity.immutable:
            problems.append(f"{IDENTITY!r} must be non-nullable and immutable")
        activity = by_name.get(ACTIVITY)
        if activity is None:
            problems.append(f"the Activity Field {ACTIVITY!r} is missing")
        elif (
            activity.type is not FieldType.BOOLEAN
            or activity.nullable
            or activity.immutable
        ):
            problems.append(f"{ACTIVITY!r} must be a non-nullable, mutable boolean")

        related: set[str] = set()
        for relation in self.relations:
            if relation.local_field not in by_name:
                problems.append(
                    f"Relation names unknown Field {relation.local_field!r}"
                )
            elif relation.local_field in related:
                problems.append(
                    f"Field {relation.local_field!r} has more than one Relation"
                )
            related.add(relation.local_field)

        for kind, entries in (
            ("Uniqueness Constraint", self.unique_constraints),
            ("Index", self.indexes),
        ):
            seen: set[tuple[str, ...]] = set()
            for entry in entries:
                if not isinstance(entry.fields, tuple) or not entry.fields:
                    problems.append(f"{kind} must name a non-empty tuple of Fields")
                    continue
                unknown = [name for name in entry.fields if name not in by_name]
                if unknown:
                    problems.append(f"{kind} names unknown Fields {unknown!r}")
                if len(set(entry.fields)) != len(entry.fields):
                    problems.append(f"{kind} {entry.fields!r} repeats a Field")
                if entry.fields in seen:
                    problems.append(
                        f"{kind} {entry.fields!r} is declared more than once"
                    )
                seen.add(entry.fields)

        if problems:
            raise DeclarationError(f"entity {self.name!r}", problems)
