"""Public Declaration contract for the logical meaning of Entities and Fields.

A Declaration is plain structured data. It chooses no table, query, storage engine,
transport, or consumer behaviour.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from types import MappingProxyType
from typing import Any, Literal, get_args

type FieldType = Literal["integer", "string", "boolean", "float", "decimal", "datetime"]
type Sensitivity = Literal["password", "sensitive"]
type ValueGeneration = Literal["auto_increment"]

_PYTHON_TYPES: dict[str, type] = {
    "integer": int,
    "string": str,
    "boolean": bool,
    "float": float,
    "decimal": Decimal,
    "datetime": datetime,
}


@dataclass(frozen=True, slots=True)
class FieldDeclaration:
    """The complete public record of one Field.

    ``has_default`` records whether a Default Value was declared, so an absent
    default differs from an explicit ``None`` default.
    """

    name: str
    type: FieldType
    nullable: bool
    description: str | None = None
    has_default: bool = False
    default: Any = None
    sensitivity: Sensitivity | None = None
    immutable: bool = False
    constraints: Mapping[str, Any] = field(default_factory=dict[str, Any])
    value_generation: ValueGeneration | None = None

    def __post_init__(self) -> None:
        if self.type not in get_args(FieldType.__value__):
            raise ValueError(f"Field {self.name!r} has an unknown type.")
        if self.sensitivity is not None and self.sensitivity not in get_args(
            Sensitivity.__value__
        ):
            raise ValueError(f"Field {self.name!r} has an unknown sensitivity.")
        if self.value_generation is not None and self.value_generation not in get_args(
            ValueGeneration.__value__
        ):
            raise ValueError(f"Field {self.name!r} has an unknown value generation.")
        if self.value_generation == "auto_increment" and self.type != "integer":
            raise ValueError(f"Field {self.name!r} auto-increments a non-integer.")
        for key, size in self.constraints.items():
            if (
                key != "size"
                or self.type != "string"
                or type(size) is not int
                or size < 1
            ):
                raise ValueError(f"Field {self.name!r} has an unsupported constraint.")
        if self.has_default and self.default is not None:
            if type(self.default) is not _PYTHON_TYPES[self.type]:
                raise ValueError(
                    f"Field {self.name!r} has a default of the wrong type."
                )
            if self.type == "datetime" and self.default.tzinfo is None:
                raise ValueError(
                    f"Field {self.name!r} has a default without a time zone."
                )
            if (
                "size" in self.constraints
                and len(self.default) != self.constraints["size"]
            ):
                raise ValueError(
                    f"Field {self.name!r} has a default of the wrong size."
                )
        if not self.has_default and self.default is not None:
            raise ValueError(f"Field {self.name!r} has a default value but no default.")
        if self.has_default and self.value_generation is not None:
            raise ValueError(f"Field {self.name!r} has a default and value generation.")
        if self.has_default and self.default is None and not self.nullable:
            raise ValueError(
                f"Field {self.name!r} has a null default but is not nullable."
            )
        object.__setattr__(
            self, "constraints", MappingProxyType(dict(self.constraints))
        )


@dataclass(frozen=True, slots=True)
class Relation:
    """Connects one local Field to a target Entity and target Field by logical name."""

    local_field: str
    target_entity: str
    target_field: str


@dataclass(frozen=True, slots=True)
class Declaration:
    """The complete public record of one Entity."""

    name: str
    description: str
    fields: tuple[FieldDeclaration, ...]
    primary_key: str
    relations: tuple[Relation, ...] = ()
    unique_constraints: tuple[tuple[str, ...], ...] = ()
    indexes: tuple[tuple[str, ...], ...] = ()

    def __post_init__(self) -> None:
        names = [declared.name for declared in self.fields]
        if len(set(names)) != len(names):
            raise ValueError(f"Entity {self.name!r} repeats a Field name.")
        for mandatory in ("id", "is_active"):
            if names.count(mandatory) != 1:
                raise ValueError(
                    f"Entity {self.name!r} needs exactly one {mandatory!r}."
                )
        if self.primary_key != "id":
            raise ValueError(f"Entity {self.name!r} must name id as its Primary Key.")
        known = set(names)
        if len({relation.local_field for relation in self.relations}) != len(
            self.relations
        ):
            raise ValueError(f"Entity {self.name!r} relates a Field more than once.")
        for relation in self.relations:
            if relation.local_field not in known:
                raise ValueError(f"Entity {self.name!r} relates unknown Field.")
        for kind, groups in (
            ("Uniqueness Constraint", self.unique_constraints),
            ("Index", self.indexes),
        ):
            if len(set(groups)) != len(groups):
                raise ValueError(f"Entity {self.name!r} repeats a {kind}.")
            for group in groups:
                if (
                    not group
                    or len(set(group)) != len(group)
                    or not known.issuperset(group)
                ):
                    raise ValueError(f"Entity {self.name!r} has an invalid {kind}.")
