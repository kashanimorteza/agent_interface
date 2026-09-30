"""Public Declaration contract: the logical meaning of Entities and Fields."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Final

TYPES: Final = (
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
VALUE_GENERATIONS: Final = ("auto_increment",)


@dataclass(frozen=True, slots=True, kw_only=True)
class FieldDeclaration:
    """Declare the complete meaning of one Field.

    Attributes:
        name (str): Logical Field name.
        description (str | None): Meaning of the Field, when stated.
        type (str): Value category, one of `TYPES`.
        nullable (bool): Whether the Field accepts a null value.
        has_default (bool): Whether a Default Value is explicitly present.
        default (Any): The Default Value; None when `has_default` is False.
        sensitivity (str | None): Sensitivity Marker, one of `SENSITIVITY_MARKERS`.
        immutable (bool): Whether the value is fixed once assigned.
        constraints (Mapping[str, Any]): Applicable value constraints by name.
        value_generation (str | None): Automatic value supply, one of
            `VALUE_GENERATIONS`.
    """

    name: str
    description: str | None = None
    type: str
    nullable: bool
    has_default: bool = False
    default: Any = None
    sensitivity: str | None = None
    immutable: bool = False
    constraints: Mapping[str, Any] = field(default_factory=dict)
    value_generation: str | None = None

    def __post_init__(self) -> None:
        label = f"Field {self.name!r}"
        if self.type not in TYPES:
            raise ValueError(f"{label} has unknown Type {self.type!r}")
        if self.sensitivity is not None and self.sensitivity not in SENSITIVITY_MARKERS:
            raise ValueError(f"{label} has unknown Sensitivity Marker")
        if (
            self.value_generation is not None
            and self.value_generation not in VALUE_GENERATIONS
        ):
            raise ValueError(f"{label} has unknown Value Generation")
        if self.has_default and self.value_generation is not None:
            raise ValueError(f"{label} has both a Default Value and Value Generation")
        if not self.has_default and self.default is not None:
            raise ValueError(f"{label} carries a default value without declaring one")
        if self.has_default and self.default is None and not self.nullable:
            raise ValueError(f"{label} has a null Default Value but is not nullable")
        object.__setattr__(
            self, "constraints", MappingProxyType(dict(self.constraints))
        )


@dataclass(frozen=True, slots=True)
class Relation:
    """Connect one local Field to a target Entity and Field by logical name.

    Attributes:
        local_field (str): Logical name of the Field in the declaring Entity.
        target_entity (str): Logical name of the target Entity.
        target_field (str): Logical name of the Field in the target Entity.
    """

    local_field: str
    target_entity: str
    target_field: str


@dataclass(frozen=True, slots=True, kw_only=True)
class Declaration:
    """Declare the complete meaning and structure of one Entity.

    Attributes:
        name (str): Logical Entity name.
        description (str): Meaning of the Entity.
        fields (tuple[FieldDeclaration, ...]): Fields in Target order.
        primary_key (str): Name of the Identity Field.
        relations (tuple[Relation, ...]): Relations in Target order.
        unique_constraints (tuple[tuple[str, ...], ...]): Ordered Field names of
            each Uniqueness Constraint.
        indexes (tuple[tuple[str, ...], ...]): Ordered Field names of each Index.
    """

    name: str
    description: str
    fields: tuple[FieldDeclaration, ...]
    primary_key: str
    relations: tuple[Relation, ...] = ()
    unique_constraints: tuple[tuple[str, ...], ...] = ()
    indexes: tuple[tuple[str, ...], ...] = ()

    def __post_init__(self) -> None:
        label = f"Entity {self.name!r}"
        names = [declared.name for declared in self.fields]
        if len(set(names)) != len(names):
            raise ValueError(f"{label} repeats a Field name")
        by_name = {declared.name: declared for declared in self.fields}
        if self.primary_key != "id" or "id" not in by_name:
            raise ValueError(f"{label} must name its id Field as Primary Key")
        identity, activity = by_name["id"], by_name.get("is_active")
        if identity.nullable or not identity.immutable:
            raise ValueError(f"{label} id must be non-nullable and immutable")
        if (
            activity is None
            or activity.type != "boolean"
            or activity.nullable
            or activity.immutable
        ):
            raise ValueError(f"{label} needs a non-nullable mutable Boolean is_active")
        for relation in self.relations:
            if relation.local_field not in by_name:
                raise ValueError(
                    f"{label} Relation local Field {relation.local_field!r} "
                    "does not resolve"
                )
        if len(set(self.relations)) != len(self.relations):
            raise ValueError(f"{label} declares a duplicate Relation")
        for kind, groups in (
            ("Uniqueness Constraint", self.unique_constraints),
            ("Index", self.indexes),
        ):
            for group in groups:
                if not group or len(set(group)) != len(group):
                    raise ValueError(f"{label} {kind} is empty or repeats a Field")
                if unresolved := [member for member in group if member not in by_name]:
                    raise ValueError(
                        f"{label} {kind} Field {unresolved[0]!r} does not resolve"
                    )
            if len(set(groups)) != len(groups):
                raise ValueError(f"{label} declares a duplicate {kind}")
