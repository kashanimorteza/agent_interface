from dataclasses import dataclass
from datetime import date, datetime, time
from decimal import Decimal
from enum import StrEnum
from typing import Final
from uuid import UUID


class FieldType(StrEnum):
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
    AUTO_INCREMENT = "auto_increment"
    GENERATED_IDENTIFIER = "generated_identifier"


class Sensitivity(StrEnum):
    PASSWORD = "password"
    SENSITIVE = "sensitive"


class _NoDefault:
    def __repr__(self) -> str:
        return "NO_DEFAULT"


NO_DEFAULT: Final = _NoDefault()


def _conforms(field_type: FieldType, value: object) -> bool:
    match field_type:
        case FieldType.STRING:
            return isinstance(value, str)
        case FieldType.INTEGER:
            return isinstance(value, int) and not isinstance(value, bool)
        case FieldType.FLOAT:
            return isinstance(value, float)
        case FieldType.DECIMAL:
            return isinstance(value, Decimal)
        case FieldType.BOOLEAN:
            return isinstance(value, bool)
        case FieldType.DATETIME:
            return isinstance(value, datetime) and value.utcoffset() is not None
        case FieldType.DATE:
            return isinstance(value, date) and not isinstance(value, datetime)
        case FieldType.TIME:
            return isinstance(value, time)
        case FieldType.UUID:
            return isinstance(value, UUID)


@dataclass(frozen=True)
class FieldConstraints:
    size: int | None = None

    def __post_init__(self) -> None:
        if self.size is not None and (
            isinstance(self.size, bool)
            or not isinstance(self.size, int)
            or self.size < 1
        ):
            raise ValueError("Constraint 'size' must be a positive integer.")


@dataclass(frozen=True)
class FieldDeclaration:
    name: str
    description: str | None
    type: FieldType
    nullable: bool
    default: object = NO_DEFAULT
    sensitivity: Sensitivity | None = None
    immutable: bool = False
    constraints: FieldConstraints = FieldConstraints()
    value_generation: ValueGeneration | None = None

    def __post_init__(self) -> None:
        try:
            object.__setattr__(self, "type", FieldType(self.type))
        except ValueError:
            raise ValueError(
                f"Field '{self.name}': unrecognized Type {self.type!r}."
            ) from None
        if self.sensitivity is not None:
            try:
                object.__setattr__(self, "sensitivity", Sensitivity(self.sensitivity))
            except ValueError:
                raise ValueError(
                    f"Field '{self.name}': unrecognized Sensitivity Marker {self.sensitivity!r}."
                ) from None
        if self.value_generation is not None:
            try:
                object.__setattr__(
                    self, "value_generation", ValueGeneration(self.value_generation)
                )
            except ValueError:
                raise ValueError(
                    f"Field '{self.name}': unrecognized Value Generation {self.value_generation!r}."
                ) from None
        if self.has_default and self.value_generation is not None:
            raise ValueError(
                f"Field '{self.name}': a Default Value and Value Generation cannot both be declared."
            )
        if self.has_default:
            if self.default is None:
                if not self.nullable:
                    raise ValueError(
                        f"Field '{self.name}': a non-nullable Field cannot default to null."
                    )
            elif not _conforms(self.type, self.default):
                raise ValueError(
                    f"Field '{self.name}': the Default Value does not satisfy Type '{self.type}'."
                )
            elif (
                self.constraints.size is not None
                and isinstance(self.default, str)
                and len(self.default) > self.constraints.size
            ):
                raise ValueError(
                    f"Field '{self.name}': the Default Value exceeds the declared size."
                )

    @property
    def has_default(self) -> bool:
        return self.default is not NO_DEFAULT

    @property
    def required(self) -> bool:
        return (
            not self.nullable and not self.has_default and self.value_generation is None
        )


IDENTITY_FIELD: Final = "id"
ACTIVITY_FIELD: Final = "is_active"


def identity() -> FieldDeclaration:
    return FieldDeclaration(
        name=IDENTITY_FIELD,
        description=None,
        type=FieldType.INTEGER,
        nullable=False,
        immutable=True,
        value_generation=ValueGeneration.AUTO_INCREMENT,
    )


def activity(description: str) -> FieldDeclaration:
    return FieldDeclaration(
        name=ACTIVITY_FIELD,
        description=description,
        type=FieldType.BOOLEAN,
        nullable=False,
        default=True,
        immutable=False,
    )


@dataclass(frozen=True)
class RelationDeclaration:
    local_field: str
    target_entity: str
    target_field: str


@dataclass(frozen=True)
class UniqueConstraintDeclaration:
    fields: tuple[str, ...]


@dataclass(frozen=True)
class IndexDeclaration:
    fields: tuple[str, ...]


@dataclass(frozen=True)
class Declaration:
    name: str
    description: str
    fields: tuple[FieldDeclaration, ...]
    primary_key: str
    relations: tuple[RelationDeclaration, ...] = ()
    unique_constraints: tuple[UniqueConstraintDeclaration, ...] = ()
    indexes: tuple[IndexDeclaration, ...] = ()

    def __post_init__(self) -> None:
        names = [field.name for field in self.fields]
        duplicated = sorted({name for name in names if names.count(name) > 1})
        if duplicated:
            raise ValueError(f"Entity '{self.name}': duplicate Fields {duplicated}.")
        if self.primary_key not in names:
            raise ValueError(
                f"Entity '{self.name}': Primary Key '{self.primary_key}' is not a Field."
            )
        if self.primary_key != IDENTITY_FIELD:
            raise ValueError(
                f"Entity '{self.name}': the Primary Key must name '{IDENTITY_FIELD}'."
            )
        by_name = {field.name: field for field in self.fields}
        identity_field = by_name[IDENTITY_FIELD]
        if identity_field.nullable or not identity_field.immutable:
            raise ValueError(
                f"Entity '{self.name}': '{IDENTITY_FIELD}' must be non-nullable and immutable."
            )
        activity_field = by_name.get(ACTIVITY_FIELD)
        if activity_field is None:
            raise ValueError(f"Entity '{self.name}': missing '{ACTIVITY_FIELD}' Field.")
        if (
            activity_field.type is not FieldType.BOOLEAN
            or activity_field.nullable
            or activity_field.immutable
        ):
            raise ValueError(
                f"Entity '{self.name}': '{ACTIVITY_FIELD}' must be a non-nullable, mutable boolean."
            )
        for relation in self.relations:
            if relation.local_field not in names:
                raise ValueError(
                    f"Entity '{self.name}': Relation local Field '{relation.local_field}' is not a Field."
                )
        if len(set(self.relations)) != len(self.relations):
            raise ValueError(f"Entity '{self.name}': duplicate Relations.")
        for kind, constraints in (
            ("Uniqueness Constraint", self.unique_constraints),
            ("Index", self.indexes),
        ):
            for constraint in constraints:
                if not constraint.fields:
                    raise ValueError(f"Entity '{self.name}': a {kind} names no Field.")
                unknown = [name for name in constraint.fields if name not in names]
                if unknown:
                    raise ValueError(
                        f"Entity '{self.name}': {kind} names unknown Fields {unknown}."
                    )
                if len(set(constraint.fields)) != len(constraint.fields):
                    raise ValueError(f"Entity '{self.name}': a {kind} repeats a Field.")
            if len(set(constraints)) != len(constraints):
                raise ValueError(f"Entity '{self.name}': duplicate {kind}s.")
