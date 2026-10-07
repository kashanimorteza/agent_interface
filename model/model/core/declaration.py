"""Public Declaration contract: the structured, immutable statement of Entity and Field meaning."""

from dataclasses import dataclass
from enum import StrEnum

from model.core import _types


class DeclarationError(ValueError):
    """Raised when a Declaration is invalid or contradictory."""


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


@dataclass(frozen=True, slots=True)
class FieldConstraints:
    """Value constraints of one Field."""

    size: int | None = None

    def __post_init__(self) -> None:
        if self.size is not None and (
            isinstance(self.size, bool)
            or not isinstance(self.size, int)
            or self.size < 1
        ):
            raise DeclarationError("A size constraint must be a positive length.")


def _field_names(owner: str, fields: object) -> None:
    if not isinstance(fields, tuple) or not fields:
        raise DeclarationError(
            f"{owner} must name a non-empty ordered tuple of Fields."
        )
    for name in fields:
        if not isinstance(name, str) or not name:
            raise DeclarationError(f"{owner} must name Fields by non-empty strings.")
    if len(set(fields)) != len(fields):
        raise DeclarationError(f"{owner} must not repeat a Field.")


@dataclass(frozen=True, slots=True)
class Relation:
    """Connects one local Field to a target Entity and target Field by logical name."""

    local_field: str
    target_entity: str
    target_field: str

    def __post_init__(self) -> None:
        for member in (self.local_field, self.target_entity, self.target_field):
            if not isinstance(member, str) or not member:
                raise DeclarationError(
                    "A Relation names its local Field, target Entity, and target Field."
                )


@dataclass(frozen=True, slots=True)
class UniqueConstraint:
    """Requires one Field or an ordered combination of Fields to be unique."""

    fields: tuple[str, ...]

    def __post_init__(self) -> None:
        _field_names("A Uniqueness Constraint", self.fields)


@dataclass(frozen=True, slots=True)
class Index:
    """Records an access intention for one Field or an ordered combination of Fields."""

    fields: tuple[str, ...]

    def __post_init__(self) -> None:
        _field_names("An Index", self.fields)


class _NoDefault:
    """The marker for a Field that declares no Default Value, distinct from an explicit null."""

    __slots__ = ()

    def __repr__(self) -> str:
        return "NO_DEFAULT"


NO_DEFAULT = _NoDefault()


@dataclass(frozen=True, slots=True)
class FieldDeclaration:
    """The complete public record of one Field's meaning."""

    name: str
    type: FieldType
    nullable: bool
    description: str | None = None
    default: object = NO_DEFAULT
    sensitivity: Sensitivity | None = None
    immutable: bool = False
    constraints: FieldConstraints = FieldConstraints()
    value_generation: ValueGeneration | None = None

    def __post_init__(self) -> None:
        name = self.name
        if not isinstance(name, str) or not name:
            raise DeclarationError("A Field name must be a non-empty string.")
        for value, kind in (
            (self.type, FieldType),
            (self.constraints, FieldConstraints),
        ):
            if not isinstance(value, kind):
                raise DeclarationError(f"Field {name}: expected a {kind.__name__}.")
        for value, kind in (
            (self.sensitivity, Sensitivity),
            (self.value_generation, ValueGeneration),
        ):
            if value is not None and not isinstance(value, kind):
                raise DeclarationError(
                    f"Field {name}: expected a {kind.__name__} or none."
                )
        if not isinstance(self.nullable, bool) or not isinstance(self.immutable, bool):
            raise DeclarationError(
                f"Field {name}: nullable and immutable must be booleans."
            )
        if self.description is not None and not isinstance(self.description, str):
            raise DeclarationError(
                f"Field {name}: the description must be a string or none."
            )
        if self.constraints.size is not None and self.type is not FieldType.string:
            raise DeclarationError(
                f"Field {name}: a size constraint applies only to a string Field."
            )
        match self.value_generation:
            case ValueGeneration.auto_increment if self.type is not FieldType.integer:
                raise DeclarationError(
                    f"Field {name}: Auto Increment requires an integer Field."
                )
            case ValueGeneration.generated_identifier if self.type not in (
                FieldType.uuid,
                FieldType.string,
            ):
                raise DeclarationError(
                    f"Field {name}: a Generated Identifier requires a uuid or string Field."
                )
        if self.has_default:
            if self.value_generation is not None:
                raise DeclarationError(
                    f"Field {name}: a Default Value cannot coexist with Value Generation."
                )
            if self.default is None:
                if not self.nullable:
                    raise DeclarationError(
                        f"Field {name}: a non-nullable Field cannot default to null."
                    )
            elif not _types.accepts(self.type, self.default):
                raise DeclarationError(
                    f"Field {name}: the Default Value does not match the Field Type."
                )

    @property
    def has_default(self) -> bool:
        """Whether a Default Value is declared, including an explicit null."""
        return self.default is not NO_DEFAULT

    @property
    def required(self) -> bool:
        """Whether construction must supply a value."""
        return (
            not self.nullable and not self.has_default and self.value_generation is None
        )


@dataclass(frozen=True, slots=True)
class EntityDeclaration:
    """The complete public record of one Entity's meaning."""

    name: str
    description: str | None
    fields: tuple[FieldDeclaration, ...]
    primary_key: str = "id"
    relations: tuple[Relation, ...] = ()
    unique_constraints: tuple[UniqueConstraint, ...] = ()
    indexes: tuple[Index, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name:
            raise DeclarationError("An Entity name must be a non-empty string.")
        name = self.name
        if self.description is not None and not isinstance(self.description, str):
            raise DeclarationError(
                f"Entity {name}: the description must be a string or none."
            )
        for members, kind, label in (
            (self.fields, FieldDeclaration, "fields"),
            (self.relations, Relation, "relations"),
            (self.unique_constraints, UniqueConstraint, "unique constraints"),
            (self.indexes, Index, "indexes"),
        ):
            if not isinstance(members, tuple) or not all(
                isinstance(m, kind) for m in members
            ):
                raise DeclarationError(
                    f"Entity {name}: {label} must be a tuple of {kind.__name__} records."
                )
        if not self.fields:
            raise DeclarationError(f"Entity {name}: an Entity needs Fields.")
        names = [f.name for f in self.fields]
        if len(set(names)) != len(names):
            raise DeclarationError(f"Entity {name}: Field names must be unique.")
        if self.primary_key != "id" or "id" not in names:
            raise DeclarationError(
                f"Entity {name}: the Primary Key must name the Field id."
            )
        identity = self.field("id")
        if identity.nullable or not identity.immutable:
            raise DeclarationError(
                f"Entity {name}: id must be non-nullable and immutable."
            )
        if "is_active" not in names:
            raise DeclarationError(
                f"Entity {name}: an Entity needs the Activity Field is_active."
            )
        activity = self.field("is_active")
        if (
            activity.type is not FieldType.boolean
            or activity.nullable
            or activity.immutable
        ):
            raise DeclarationError(
                f"Entity {name}: is_active must be a non-nullable, mutable boolean."
            )
        known = set(names)
        local = [r.local_field for r in self.relations]
        if not known.issuperset(local):
            raise DeclarationError(
                f"Entity {name}: a Relation names an unknown local Field."
            )
        if len(set(local)) != len(local):
            raise DeclarationError(
                f"Entity {name}: a local Field has at most one Relation."
            )
        for entries, label in (
            (self.unique_constraints, "Uniqueness Constraint"),
            (self.indexes, "Index"),
        ):
            combos = [e.fields for e in entries]
            if not all(known.issuperset(c) for c in combos):
                raise DeclarationError(
                    f"Entity {name}: a {label} names an unknown Field."
                )
            if len(set(combos)) != len(combos):
                raise DeclarationError(
                    f"Entity {name}: a {label} duplicates another entry."
                )

    @property
    def field_names(self) -> tuple[str, ...]:
        """The Field names in Declaration order."""
        return tuple(f.name for f in self.fields)

    def field(self, name: str) -> FieldDeclaration:
        """The Field Declaration with the given name."""
        for declared in self.fields:
            if declared.name == name:
                return declared
        raise KeyError(name)
