"""Declaration layer.

Records the technology-independent meaning and metadata of an Entity: its Identity
and Primary Key, Fields with their Types and Field Rules, References, Uniqueness
Constraints, Index intentions, and Value Generation. Declaration holds no runtime
behaviour and chooses no storage technology.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import Enum, StrEnum
from typing import Any, Final


class FieldType(StrEnum):
    """Technology-independent category of values a Field may hold."""

    INTEGER = "integer"
    STRING = "string"
    BOOLEAN = "boolean"
    DECIMAL = "decimal"
    FLOAT = "float"
    DATETIME = "datetime"


class Sensitivity(StrEnum):
    """Sensitivity Marker: a value category that Model records but never handles."""

    PASSWORD = "password"
    SENSITIVE = "sensitive"


class ValueGeneration(StrEnum):
    """A declared way to supply a Field value automatically when an Entity is created."""

    AUTO_INCREMENT = "auto_increment"
    GENERATED_IDENTIFIER = "generated_identifier"


class _NoDefault(Enum):
    """Marker meaning that a Field declares no Default Value (distinct from a default of None)."""

    NO_DEFAULT = "NO_DEFAULT"


NO_DEFAULT: Final = _NoDefault.NO_DEFAULT

IDENTITY: Final = "id"


@dataclass(frozen=True, slots=True)
class FieldDeclaration:
    """One named value of an Entity with its Type and Field Rules."""

    name: str
    type: FieldType
    nullable: bool = False
    default: Any = NO_DEFAULT
    sensitivity: Sensitivity | None = None
    immutable: bool = False
    length: int | None = None
    constraints: Mapping[str, Any] = field(default_factory=dict)
    value_generation: ValueGeneration | None = None

    def __post_init__(self) -> None:
        if self.value_generation is not None and self.default is not NO_DEFAULT:
            raise ValueError(
                f"Field '{self.name}' cannot declare both Value Generation and a Default Value"
            )

    @property
    def has_default(self) -> bool:
        return self.default is not NO_DEFAULT


@dataclass(frozen=True, slots=True)
class Reference:
    """A Field-level Reference holding another Entity's `id`."""

    field: str
    entity: str
    target_field: str = IDENTITY


@dataclass(frozen=True, slots=True)
class Unique:
    """A Uniqueness Constraint over one Field or a combination of Fields."""

    fields: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Index:
    """An Index intention over one Field or a combination of Fields."""

    fields: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Declaration:
    """The complete technology-independent meaning of one Entity."""

    entity: str
    fields: tuple[FieldDeclaration, ...]
    references: tuple[Reference, ...] = ()
    uniques: tuple[Unique, ...] = ()
    indexes: tuple[Index, ...] = ()

    def __post_init__(self) -> None:
        names = [f.name for f in self.fields]
        if len(set(names)) != len(names):
            raise ValueError(
                f"Entity '{self.entity}' declares a Field name more than once"
            )
        if IDENTITY not in names:
            raise ValueError(
                f"Entity '{self.entity}' must declare the '{IDENTITY}' Identity Field"
            )
        for reference in self.references:
            if reference.field not in names:
                raise ValueError(
                    f"Entity '{self.entity}' references from unknown Field '{reference.field}'"
                )
            if reference.target_field != IDENTITY:
                raise ValueError(
                    f"A Reference must identify the target Entity's '{IDENTITY}'"
                )
        for constraint in (*self.uniques, *self.indexes):
            for name in constraint.fields:
                if name not in names:
                    raise ValueError(
                        f"Entity '{self.entity}' declares a constraint over unknown Field '{name}'"
                    )

    @property
    def identity(self) -> str:
        return IDENTITY

    @property
    def primary_key(self) -> str:
        return IDENTITY

    @property
    def value_generation(self) -> Mapping[str, ValueGeneration]:
        return {
            f.name: f.value_generation
            for f in self.fields
            if f.value_generation is not None
        }

    def get_field(self, name: str) -> FieldDeclaration:
        for declared in self.fields:
            if declared.name == name:
                return declared
        raise KeyError(name)
