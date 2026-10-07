"""Public Declaration contract: immutable records of Field and Entity meaning."""

import math
from dataclasses import dataclass
from datetime import date, datetime, time
from decimal import Decimal
from enum import StrEnum
from typing import Final
from uuid import UUID


class DeclarationError(ValueError):
    """A Declaration is invalid or contradictory and cannot be created."""


class FieldType(StrEnum):
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
    auto_increment = "auto_increment"
    generated_identifier = "generated_identifier"


class Sensitivity(StrEnum):
    password = "password"
    sensitive = "sensitive"


class _NoDefault:
    """The type of NO_DEFAULT, which marks a Field with no Default Value."""

    _instance: "_NoDefault | None" = None

    def __new__(cls) -> "_NoDefault":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        return "NO_DEFAULT"

    def __bool__(self) -> bool:
        return False


NO_DEFAULT: Final = _NoDefault()


@dataclass(frozen=True, slots=True)
class FieldConstraints:
    size: int | None = None

    def __post_init__(self) -> None:
        size = self.size
        if size is not None and (
            not isinstance(size, int) or isinstance(size, bool) or size < 1
        ):
            raise DeclarationError("A size constraint must be a positive length.")


def _matches_type(value: object, field_type: FieldType) -> bool:
    match field_type:
        case FieldType.string:
            return isinstance(value, str)
        case FieldType.integer:
            return isinstance(value, int) and not isinstance(value, bool)
        case FieldType.float:
            return isinstance(value, float) and math.isfinite(value)
        case FieldType.decimal:
            return isinstance(value, Decimal) and value.is_finite()
        case FieldType.boolean:
            return isinstance(value, bool)
        case FieldType.datetime:
            return (
                isinstance(value, datetime)
                and value.tzinfo is not None
                and value.utcoffset() is not None
            )
        case FieldType.date:
            return isinstance(value, date) and not isinstance(value, datetime)
        case FieldType.time:
            return isinstance(value, time)
        case FieldType.uuid:
            return isinstance(value, UUID)


@dataclass(frozen=True, slots=True)
class FieldDeclaration:
    name: str
    type: FieldType
    nullable: bool
    description: str | None
    default: object = NO_DEFAULT
    sensitivity: Sensitivity | None = None
    immutable: bool = False
    constraints: FieldConstraints = FieldConstraints()
    value_generation: ValueGeneration | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name:
            raise DeclarationError("A Field name must be a non-empty string.")
        field = f"Field {self.name!r}"
        if not isinstance(self.type, FieldType):
            raise DeclarationError(f"{field} has an unknown Type.")
        if not isinstance(self.nullable, bool):
            raise DeclarationError(f"{field} must state nullability as a boolean.")
        if self.description is not None and not isinstance(self.description, str):
            raise DeclarationError(f"{field} description must be a string or absent.")
        if self.sensitivity is not None and not isinstance(
            self.sensitivity, Sensitivity
        ):
            raise DeclarationError(f"{field} has an unrecognized Sensitivity Marker.")
        if not isinstance(self.immutable, bool):
            raise DeclarationError(f"{field} must state immutability as a boolean.")
        if not isinstance(self.constraints, FieldConstraints):
            raise DeclarationError(f"{field} constraints must be FieldConstraints.")
        if self.constraints.size is not None and self.type is not FieldType.string:
            raise DeclarationError(f"{field} has a size constraint but is no string.")
        self._check_value_generation(field)
        self._check_default(field)

    def _check_value_generation(self, field: str) -> None:
        generation = self.value_generation
        if generation is None:
            return
        if not isinstance(generation, ValueGeneration):
            raise DeclarationError(f"{field} has an unknown Value Generation.")
        if self.default is not NO_DEFAULT:
            raise DeclarationError(f"{field} has a Default Value and Value Generation.")
        if generation is ValueGeneration.auto_increment:
            if self.type is not FieldType.integer:
                raise DeclarationError(f"{field} uses Auto Increment, not integer.")
        elif self.type not in (FieldType.uuid, FieldType.string):
            raise DeclarationError(
                f"{field} uses a Generated Identifier, neither uuid nor string."
            )

    def _check_default(self, field: str) -> None:
        default = self.default
        if default is NO_DEFAULT:
            return
        if default is None:
            if not self.nullable:
                raise DeclarationError(f"{field} has a null default, not nullable.")
        elif not _matches_type(default, self.type):
            raise DeclarationError(f"{field} has a default not matching its Type.")
        elif (
            self.constraints.size is not None
            and isinstance(default, str)
            and len(default) > self.constraints.size
        ):
            raise DeclarationError(f"{field} has a default beyond its size.")


@dataclass(frozen=True, slots=True)
class Relation:
    local_field: str
    target_entity: str
    target_field: str

    def __post_init__(self) -> None:
        members = (self.local_field, self.target_entity, self.target_field)
        if not all(isinstance(member, str) and member for member in members):
            raise DeclarationError("A Relation names a local Field and a target.")


def _ordered_sets(entries: object, kind: str) -> tuple[tuple[str, ...], ...]:
    if not isinstance(entries, (tuple, list)):
        raise DeclarationError(f"{kind} must be an ordered collection.")
    result = []
    for entry in entries:
        if not isinstance(entry, (tuple, list)):
            raise DeclarationError(f"Each {kind} entry must be a Field collection.")
        result.append(tuple(entry))
    return tuple(result)


@dataclass(frozen=True, slots=True)
class Declaration:
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
        entity = f"Entity {self.name!r}"
        if not isinstance(self.description, str) or not self.description:
            raise DeclarationError(f"{entity} must have a description.")
        if not isinstance(self.fields, (tuple, list)) or not all(
            isinstance(field, FieldDeclaration) for field in self.fields
        ):
            raise DeclarationError(f"{entity} fields must be Field Declarations.")
        if not isinstance(self.relations, (tuple, list)) or not all(
            isinstance(relation, Relation) for relation in self.relations
        ):
            raise DeclarationError(f"{entity} relations must be Relations.")
        object.__setattr__(self, "fields", tuple(self.fields))
        object.__setattr__(self, "relations", tuple(self.relations))
        object.__setattr__(
            self,
            "unique_constraints",
            _ordered_sets(self.unique_constraints, "Uniqueness Constraints"),
        )
        object.__setattr__(self, "indexes", _ordered_sets(self.indexes, "Indexes"))

        by_name = {field.name: field for field in self.fields}
        if len(by_name) != len(self.fields):
            raise DeclarationError(f"{entity} has duplicate Field names.")
        self._check_identity(entity, by_name)
        self._check_relations(entity, by_name)
        self._check_field_sets(entity, by_name)

    def _check_identity(
        self, entity: str, by_name: dict[str, FieldDeclaration]
    ) -> None:
        if self.primary_key != "id":
            raise DeclarationError(f"{entity} must name id as its Primary Key.")
        identity = by_name.get("id")
        if identity is None or identity.nullable or not identity.immutable:
            raise DeclarationError(f"{entity} needs a non-nullable immutable id.")
        activity = by_name.get("is_active")
        if (
            activity is None
            or activity.type is not FieldType.boolean
            or activity.nullable
            or activity.immutable
        ):
            raise DeclarationError(f"{entity} needs a mutable boolean is_active.")

    def _check_relations(
        self, entity: str, by_name: dict[str, FieldDeclaration]
    ) -> None:
        related: set[str] = set()
        for relation in self.relations:
            local = relation.local_field
            if local not in by_name:
                raise DeclarationError(f"{entity} has a Relation on unknown {local!r}.")
            if local in related:
                raise DeclarationError(f"{entity} has two Relations on {local!r}.")
            related.add(local)

    def _check_field_sets(
        self, entity: str, by_name: dict[str, FieldDeclaration]
    ) -> None:
        kinds = (
            ("Uniqueness Constraint", self.unique_constraints),
            ("Index", self.indexes),
        )
        for kind, entries in kinds:
            seen: set[tuple[str, ...]] = set()
            for entry in entries:
                if not entry:
                    raise DeclarationError(f"{entity} has an empty {kind}.")
                unknown = [name for name in entry if name not in by_name]
                if unknown:
                    raise DeclarationError(f"{entity} {kind} names {unknown[0]!r}.")
                if len(set(entry)) != len(entry):
                    raise DeclarationError(f"{entity} {kind} repeats a Field.")
                if entry in seen:
                    raise DeclarationError(f"{entity} has a duplicate {kind}.")
                seen.add(entry)
