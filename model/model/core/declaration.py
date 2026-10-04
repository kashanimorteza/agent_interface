"""Public Declaration contract: the complete logical meaning of an Entity and its Fields."""

from dataclasses import dataclass
from datetime import date, datetime, time
from decimal import Decimal
from typing import Final, Self
from uuid import UUID

FIELD_TYPES: Final = (
    "string",
    "integer",
    "float",
    "decimal",
    "boolean",
    "datetime",
    "date",
    "time",
    "uuid",
)
SENSITIVITY_MARKERS: Final = ("password", "sensitive")
VALUE_GENERATIONS: Final = ("auto_increment", "generated_identifier")

_PYTHON_TYPES: Final = {
    "string": str,
    "integer": int,
    "float": float,
    "decimal": Decimal,
    "boolean": bool,
    "datetime": datetime,
    "date": date,
    "time": time,
    "uuid": UUID,
}


class _NoDefault:
    """Marks a Field that declares no Default Value, which differs from an explicit null."""

    _instance: Self | None = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        return "NO_DEFAULT"

    def __bool__(self) -> bool:
        return False


NO_DEFAULT: Final = _NoDefault()


@dataclass(frozen=True)
class FieldDeclaration:
    """The complete public record of one Field."""

    name: str
    description: str | None
    type: str
    nullable: bool
    default: object = NO_DEFAULT
    sensitivity: str | None = None
    immutable: bool = False
    constraints: tuple[tuple[str, object], ...] = ()
    value_generation: str | None = None

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("A Field name must not be empty.")
        if self.type not in FIELD_TYPES:
            raise ValueError(
                f"Field '{self.name}' declares unknown type '{self.type}'."
            )
        if self.sensitivity is not None and self.sensitivity not in SENSITIVITY_MARKERS:
            raise ValueError(
                f"Field '{self.name}' declares an unrecognized sensitivity marker."
            )
        if (
            self.value_generation is not None
            and self.value_generation not in VALUE_GENERATIONS
        ):
            raise ValueError(
                f"Field '{self.name}' declares unknown value generation '{self.value_generation}'."
            )
        if self.default is not NO_DEFAULT and self.value_generation is not None:
            raise ValueError(
                f"Field '{self.name}' declares both a Default Value and Value Generation."
            )
        if self.default is not NO_DEFAULT:
            self._check_default()

    def _check_default(self) -> None:
        if self.default is None:
            if not self.nullable:
                raise ValueError(
                    f"Field '{self.name}' is not nullable and cannot default to null."
                )
            return
        expected = _PYTHON_TYPES[self.type]
        valid = isinstance(self.default, expected) and (
            expected is bool or not isinstance(self.default, bool)
        )
        if (
            self.type == "float"
            and isinstance(self.default, int)
            and not isinstance(self.default, bool)
        ):
            valid = True
        if not valid:
            raise ValueError(
                f"Default Value of Field '{self.name}' does not match its type '{self.type}'."
            )


@dataclass(frozen=True)
class RelationDeclaration:
    """One Relation from a local Field to a target Entity and target Field by logical name."""

    local_field: str
    target_entity: str
    target_field: str


@dataclass(frozen=True)
class Declaration:
    """The complete public record of one Entity."""

    name: str
    description: str
    fields: tuple[FieldDeclaration, ...]
    primary_key: str
    relations: tuple[RelationDeclaration, ...] = ()
    unique_constraints: tuple[tuple[str, ...], ...] = ()
    indexes: tuple[tuple[str, ...], ...] = ()

    def __post_init__(self) -> None:
        names = [field.name for field in self.fields]
        if len(set(names)) != len(names):
            raise ValueError(f"Entity '{self.name}' repeats a Field name.")
        known = set(names)
        if self.primary_key not in known:
            raise ValueError(
                f"Entity '{self.name}' names a Primary Key that is not one of its Fields."
            )
        local_fields = [relation.local_field for relation in self.relations]
        if len(set(local_fields)) != len(local_fields):
            raise ValueError(f"Entity '{self.name}' repeats a Relation.")
        for relation in self.relations:
            if relation.local_field not in known:
                raise ValueError(
                    f"Entity '{self.name}' has a Relation on an unknown Field."
                )
        for label, groups in (
            ("Uniqueness Constraint", self.unique_constraints),
            ("Index", self.indexes),
        ):
            if len(set(groups)) != len(groups):
                raise ValueError(f"Entity '{self.name}' repeats a {label}.")
            for group in groups:
                if (
                    not group
                    or len(set(group)) != len(group)
                    or not set(group) <= known
                ):
                    raise ValueError(f"Entity '{self.name}' has an invalid {label}.")

    def field(self, name: str) -> FieldDeclaration:
        """Return the Field Declaration with the given logical name."""
        for field in self.fields:
            if field.name == name:
                return field
        raise KeyError(name)


def validate_relations(declarations: tuple[Declaration, ...]) -> None:
    """Fail unless every Relation target resolves within the Model with a compatible Type."""
    by_name = {declaration.name: declaration for declaration in declarations}
    for declaration in declarations:
        for relation in declaration.relations:
            target = by_name.get(relation.target_entity)
            if target is None:
                raise ValueError(
                    f"Entity '{declaration.name}' relates to unknown Entity '{relation.target_entity}'."
                )
            try:
                target_field = target.field(relation.target_field)
            except KeyError:
                raise ValueError(
                    f"Entity '{declaration.name}' relates to unknown Field '{relation.target_entity}.{relation.target_field}'."
                ) from None
            if target_field.type != declaration.field(relation.local_field).type:
                raise ValueError(
                    f"Relation '{declaration.name}.{relation.local_field}' has an incompatible endpoint Type."
                )
