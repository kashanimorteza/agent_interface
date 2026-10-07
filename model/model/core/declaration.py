"""Declaration contract: the public, immutable description of every Entity and its Fields."""

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Final

from ._types import matches


class DeclarationError(ValueError):
    """A Declaration breaks a structural rule of the Declaration contract."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise DeclarationError(message)


def _member[E: StrEnum](enum: type[E], value: Any) -> E | None:
    try:
        return enum(value)
    except TypeError, ValueError:
        return None


def _is_name(value: Any) -> bool:
    return isinstance(value, str) and value != ""


def _check_fields(owner: str, fields: Any) -> None:
    _require(
        isinstance(fields, tuple) and len(fields) > 0,
        f"{owner} must name a non-empty tuple of Fields",
    )
    _require(
        all(_is_name(name) for name in fields),
        f"{owner} must name Fields by non-empty strings",
    )
    _require(len(set(fields)) == len(fields), f"{owner} must not repeat a Field")


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


class _Absent:
    """Marks a Field Declaration that has no Default Value, as distinct from an explicit null default."""

    __slots__ = ()

    def __repr__(self) -> str:
        return "ABSENT"

    def __bool__(self) -> bool:
        return False

    def __copy__(self) -> _Absent:
        return self

    def __deepcopy__(self, memo: dict[int, Any]) -> _Absent:
        return self

    def __reduce__(self) -> str:
        return "ABSENT"


ABSENT: Final = _Absent()


@dataclass(frozen=True, slots=True)
class FieldConstraints:
    """Value constraints of a Field."""

    size: int | None = None


@dataclass(frozen=True, slots=True)
class FieldDeclaration:
    """The complete public record of one Field."""

    name: str
    type: FieldType
    nullable: bool
    description: str | None
    default: Any = ABSENT
    sensitivity: Sensitivity | None = None
    immutable: bool = False
    constraints: FieldConstraints = FieldConstraints()
    value_generation: ValueGeneration | None = None

    def __post_init__(self) -> None:
        _require(_is_name(self.name), "A Field name must be a non-empty string")
        where = f"Field {self.name!r}"
        field_type = _member(FieldType, self.type)
        if field_type is None:
            raise DeclarationError(f"{where} names a Type outside the closed set")
        _require(
            isinstance(self.nullable, bool), f"{where} must state nullable as a boolean"
        )
        _require(
            self.description is None or isinstance(self.description, str),
            f"{where} must describe itself with a string or nothing",
        )
        _require(
            self.sensitivity is None
            or _member(Sensitivity, self.sensitivity) is not None,
            f"{where} names an unrecognized Sensitivity Marker",
        )
        _require(
            isinstance(self.immutable, bool),
            f"{where} must state immutable as a boolean",
        )
        _require(
            isinstance(self.constraints, FieldConstraints),
            f"{where} must hold Field constraints",
        )
        size = self.constraints.size
        if size is not None:
            _require(
                isinstance(size, int) and not isinstance(size, bool) and size > 0,
                f"{where} must have a positive size",
            )
            _require(
                field_type is FieldType.string,
                f"{where} has a size but is not a string",
            )
        generation = None
        if self.value_generation is not None:
            generation = _member(ValueGeneration, self.value_generation)
            _require(
                generation is not None, f"{where} names an unknown Value Generation"
            )
        if generation is ValueGeneration.auto_increment:
            _require(
                field_type is FieldType.integer,
                f"{where} uses Auto Increment but is not an integer",
            )
        if generation is ValueGeneration.generated_identifier:
            _require(
                field_type in (FieldType.uuid, FieldType.string),
                f"{where} uses a Generated Identifier but is not a uuid or string",
            )
        if self.default is not ABSENT:
            _require(
                generation is None,
                f"{where} has both a Default Value and Value Generation",
            )
            if self.default is None:
                _require(
                    self.nullable, f"{where} has a null default but is not nullable"
                )
            else:
                _require(
                    matches(field_type, self.default),
                    f"{where} has a Default Value that does not match its Type",
                )
                _require(
                    size is None or len(self.default) <= size,
                    f"{where} has a Default Value longer than its size",
                )


@dataclass(frozen=True, slots=True)
class Relation:
    """Connects one local Field to a target Entity and target Field by logical name."""

    local_field: str
    target_entity: str
    target_field: str

    def __post_init__(self) -> None:
        _require(
            _is_name(self.local_field)
            and _is_name(self.target_entity)
            and _is_name(self.target_field),
            "A Relation must name its local Field, target Entity, and target Field",
        )


@dataclass(frozen=True, slots=True)
class UniquenessConstraint:
    """Requires one Field or an ordered combination of Fields to be unique."""

    fields: tuple[str, ...]

    def __post_init__(self) -> None:
        _check_fields("A Uniqueness Constraint", self.fields)


@dataclass(frozen=True, slots=True)
class Index:
    """Records an access intention for one Field or an ordered combination of Fields."""

    fields: tuple[str, ...]

    def __post_init__(self) -> None:
        _check_fields("An Index", self.fields)


@dataclass(frozen=True, slots=True)
class Declaration:
    """The complete public record of one Entity: its Fields and its Entity Metadata."""

    name: str
    description: str | None
    fields: tuple[FieldDeclaration, ...]
    primary_key: str
    relations: tuple[Relation, ...] = ()
    unique_constraints: tuple[UniquenessConstraint, ...] = ()
    indexes: tuple[Index, ...] = ()

    def __post_init__(self) -> None:
        _require(_is_name(self.name), "An Entity name must be a non-empty string")
        where = f"Entity {self.name!r}"
        _require(
            self.description is None or isinstance(self.description, str),
            f"{where} must describe itself with a string or nothing",
        )
        _require(
            isinstance(self.fields, tuple) and len(self.fields) > 0,
            f"{where} must declare a non-empty tuple of Fields",
        )
        _require(
            all(isinstance(item, FieldDeclaration) for item in self.fields),
            f"{where} must declare Fields as Field Declarations",
        )
        _require(
            isinstance(self.relations, tuple)
            and all(isinstance(item, Relation) for item in self.relations),
            f"{where} must declare Relations as a tuple of Relations",
        )
        _require(
            isinstance(self.unique_constraints, tuple)
            and all(
                isinstance(item, UniquenessConstraint)
                for item in self.unique_constraints
            ),
            f"{where} must declare Uniqueness Constraints as a tuple of Uniqueness Constraints",
        )
        _require(
            isinstance(self.indexes, tuple)
            and all(isinstance(item, Index) for item in self.indexes),
            f"{where} must declare Indexes as a tuple of Indexes",
        )

        names = [item.name for item in self.fields]
        _require(len(set(names)) == len(names), f"{where} repeats a Field name")
        by_name = {item.name: item for item in self.fields}

        _require(self.primary_key == "id", f"{where} must name id as its Primary Key")
        identity = by_name.get("id")
        _require(
            identity is not None and not identity.nullable and identity.immutable,
            f"{where} must declare id as a non-nullable, immutable Field",
        )
        activity = by_name.get("is_active")
        _require(
            activity is not None
            and activity.type == FieldType.boolean
            and not activity.nullable
            and not activity.immutable,
            f"{where} must declare is_active as a non-nullable, mutable boolean Field",
        )

        local_fields = [item.local_field for item in self.relations]
        _require(
            all(name in by_name for name in local_fields),
            f"{where} has a Relation from an unknown Field",
        )
        _require(
            len(set(local_fields)) == len(local_fields),
            f"{where} has more than one Relation from a Field",
        )
        for label, entries in (
            ("Uniqueness Constraint", self.unique_constraints),
            ("Index", self.indexes),
        ):
            _require(
                all(name in by_name for entry in entries for name in entry.fields),
                f"{where} has a {label} on an unknown Field",
            )
            keys = [entry.fields for entry in entries]
            _require(len(set(keys)) == len(keys), f"{where} duplicates a {label}")
