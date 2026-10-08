"""Public Declaration contract: the structured, immutable record of Entity and Field meaning."""

import math
from dataclasses import dataclass
from datetime import date, datetime, time
from decimal import Decimal
from enum import StrEnum
from typing import Any, Final
from uuid import UUID


class DeclarationError(ValueError):
    """An invalid or contradictory Declaration."""


class FieldType(StrEnum):
    """The closed set of Field Types."""

    string = "string"
    integer = "integer"
    float = "float"
    decimal = "decimal"
    boolean = "boolean"
    datetime = "datetime"
    date = "date"
    time = "time"
    uuid = "uuid"


class ValueGeneration(StrEnum):
    """The declared ways a Field value is supplied automatically."""

    auto_increment = "auto_increment"
    generated_identifier = "generated_identifier"


class Sensitivity(StrEnum):
    """The recognized Sensitivity Markers."""

    password = "password"
    sensitive = "sensitive"


class _NoDefault:
    """Marks a Field Declaration that states no Default Value, as distinct from an explicit null default."""

    __slots__ = ()

    def __repr__(self) -> str:
        return "NO_DEFAULT"


NO_DEFAULT: Final = _NoDefault()

_VALUE_CLASSES: Final[dict[FieldType, type]] = {
    FieldType.string: str,
    FieldType.integer: int,
    FieldType.float: float,
    FieldType.decimal: Decimal,
    FieldType.boolean: bool,
    FieldType.datetime: datetime,
    FieldType.date: date,
    FieldType.time: time,
    FieldType.uuid: UUID,
}


def value_class(field_type: FieldType) -> type:
    """Return the Python class of values of a Field Type."""
    return _VALUE_CLASSES[field_type]


def conforms(field_type: FieldType, value: Any) -> bool:
    """Return whether a non-null value is exactly a value of the Field Type, without coercion."""
    if not isinstance(value, _VALUE_CLASSES[field_type]):
        return False
    match field_type:
        case FieldType.integer:
            return not isinstance(value, bool)
        case FieldType.float:
            return math.isfinite(value)
        case FieldType.decimal:
            return value.is_finite()
        case FieldType.datetime:
            return value.utcoffset() is not None
        case FieldType.date:
            return not isinstance(value, datetime)
        case _:
            return True


@dataclass(frozen=True, slots=True)
class FieldConstraints:
    """The value constraints of a Field."""

    size: int | None = None

    def __post_init__(self) -> None:
        if self.size is not None and (
            not isinstance(self.size, int)
            or isinstance(self.size, bool)
            or self.size <= 0
        ):
            raise DeclarationError("A size constraint must be a positive length.")


@dataclass(frozen=True, slots=True)
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
        name = self.name
        if not isinstance(name, str) or not name:
            raise DeclarationError("A Field name must be a non-empty string.")
        if not isinstance(self.type, FieldType):
            raise DeclarationError(
                f"Field '{name}' has a Type outside the closed set of Field Types."
            )
        if not isinstance(self.nullable, bool) or not isinstance(self.immutable, bool):
            raise DeclarationError(
                f"Field '{name}' must state nullability and immutability as booleans."
            )
        if self.description is not None and not isinstance(self.description, str):
            raise DeclarationError(
                f"Field '{name}' has a description that is not a string."
            )
        if self.sensitivity is not None and not isinstance(
            self.sensitivity, Sensitivity
        ):
            raise DeclarationError(
                f"Field '{name}' has an unrecognized Sensitivity Marker."
            )
        if not isinstance(self.constraints, FieldConstraints):
            raise DeclarationError(
                f"Field '{name}' has constraints that are not Field Constraints."
            )
        if self.constraints.size is not None and self.type is not FieldType.string:
            raise DeclarationError(
                f"Field '{name}' has a size constraint but is not a string Field."
            )
        generation = self.value_generation
        if generation is not None:
            if not isinstance(generation, ValueGeneration):
                raise DeclarationError(
                    f"Field '{name}' has an unknown Value Generation."
                )
            if self.default is not NO_DEFAULT:
                raise DeclarationError(
                    f"Field '{name}' has both a Default Value and Value Generation."
                )
            if (
                generation is ValueGeneration.auto_increment
                and self.type is not FieldType.integer
            ):
                raise DeclarationError(
                    f"Field '{name}' uses Auto Increment but is not an integer Field."
                )
            if generation is ValueGeneration.generated_identifier and self.type not in (
                FieldType.uuid,
                FieldType.string,
            ):
                raise DeclarationError(
                    f"Field '{name}' uses a Generated Identifier but is not a uuid or string Field."
                )
        if self.default is not NO_DEFAULT:
            self._check_default()

    def _check_default(self) -> None:
        if self.default is None:
            if not self.nullable:
                raise DeclarationError(
                    f"Field '{self.name}' is non-nullable but has a null Default Value."
                )
            return
        if not conforms(self.type, self.default):
            raise DeclarationError(
                f"Field '{self.name}' has a Default Value that does not match its Type."
            )
        size = self.constraints.size
        if size is not None and len(self.default) > size:
            raise DeclarationError(
                f"Field '{self.name}' has a Default Value longer than its size."
            )


@dataclass(frozen=True, slots=True)
class Relation:
    """Connects one local Field to a target Entity and target Field by logical name."""

    local_field: str
    target_entity: str
    target_field: str

    def __post_init__(self) -> None:
        for value in (self.local_field, self.target_entity, self.target_field):
            if not isinstance(value, str) or not value:
                raise DeclarationError(
                    "A Relation names a local Field, a target Entity and a target Field."
                )


@dataclass(frozen=True, slots=True)
class Declaration:
    """The complete public record of one Entity: name, description, ordered Fields and Entity Metadata."""

    name: str
    description: str
    fields: tuple[FieldDeclaration, ...]
    primary_key: str
    relations: tuple[Relation, ...] = ()
    unique_constraints: tuple[tuple[str, ...], ...] = ()
    indexes: tuple[tuple[str, ...], ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name:
            raise DeclarationError("An Entity name must be a non-empty string.")
        name = self.name
        if not isinstance(self.description, str):
            raise DeclarationError(f"Entity '{name}' must have a description.")
        for collection in (
            self.fields,
            self.relations,
            self.unique_constraints,
            self.indexes,
        ):
            if not isinstance(collection, tuple):
                raise DeclarationError(
                    f"Entity '{name}' must state its collections as tuples."
                )
        if not all(isinstance(field, FieldDeclaration) for field in self.fields):
            raise DeclarationError(
                f"Entity '{name}' has an item that is not a Field Declaration."
            )
        if not all(isinstance(relation, Relation) for relation in self.relations):
            raise DeclarationError(
                f"Entity '{name}' has an item that is not a Relation."
            )

        names = [field.name for field in self.fields]
        if len(set(names)) != len(names):
            raise DeclarationError(f"Entity '{name}' repeats a Field name.")
        by_name = {field.name: field for field in self.fields}

        if self.primary_key != "id":
            raise DeclarationError(f"Entity '{name}' must name id as its Primary Key.")
        identity = by_name.get("id")
        if identity is None or identity.nullable or not identity.immutable:
            raise DeclarationError(
                f"Entity '{name}' must have a non-nullable, immutable id Field."
            )
        activity = by_name.get("is_active")
        if (
            activity is None
            or activity.type is not FieldType.boolean
            or activity.nullable
            or activity.immutable
        ):
            raise DeclarationError(
                f"Entity '{name}' must have a non-nullable, mutable boolean is_active Field."
            )

        local_fields = [relation.local_field for relation in self.relations]
        if any(local not in by_name for local in local_fields):
            raise DeclarationError(
                f"Entity '{name}' has a Relation on an unknown local Field."
            )
        if len(set(local_fields)) != len(local_fields):
            raise DeclarationError(
                f"Entity '{name}' has more than one Relation on one local Field."
            )

        for label, entries in (
            ("Uniqueness Constraint", self.unique_constraints),
            ("Index", self.indexes),
        ):
            for entry in entries:
                if not isinstance(entry, tuple) or not entry:
                    raise DeclarationError(
                        f"Entity '{name}' has an empty or malformed {label}."
                    )
                if any(field not in by_name for field in entry):
                    raise DeclarationError(
                        f"Entity '{name}' has a {label} on an unknown Field."
                    )
                if len(set(entry)) != len(entry):
                    raise DeclarationError(
                        f"Entity '{name}' has a {label} that repeats a Field."
                    )
            if len(set(entries)) != len(entries):
                raise DeclarationError(f"Entity '{name}' has a duplicate {label}.")
