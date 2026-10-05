from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any

from pydantic import ConfigDict, TypeAdapter

from model.core._naming import entity_class_name, field_attribute_name
from model.core._types import realize

SENSITIVITY_MARKERS = ("password", "sensitive")
VALUE_GENERATIONS = ("auto_increment", "generated_identifier")
CONSTRAINTS = ("size",)

_DEFAULT_CHECK = ConfigDict(hide_input_in_errors=True)


@dataclass(frozen=True, slots=True)
class FieldDeclaration:
    name: str
    description: str | None
    type: str
    nullable: bool
    has_default: bool = False
    default: Any = None
    sensitivity: str | None = None
    immutable: bool = False
    constraints: Mapping[str, Any] = field(default_factory=dict)
    value_generation: str | None = None

    def __post_init__(self) -> None:
        python_type = realize(self.type)
        if self.sensitivity is not None and self.sensitivity not in SENSITIVITY_MARKERS:
            raise ValueError(f"Field '{self.name}' declares an unrecognized Sensitivity Marker")
        if self.value_generation is not None and self.value_generation not in VALUE_GENERATIONS:
            raise ValueError(f"Field '{self.name}' declares an unrecognized Value Generation")
        if self.has_default and self.value_generation is not None:
            raise ValueError(f"Field '{self.name}' cannot have both a Default Value and Value Generation")
        if not self.has_default and self.default is not None:
            raise ValueError(f"Field '{self.name}' carries a default value without declaring one")
        unknown = set(self.constraints) - set(CONSTRAINTS)
        if unknown:
            raise ValueError(f"Field '{self.name}' declares an unrecognized constraint: {', '.join(sorted(unknown))}")
        if self.has_default:
            if self.default is None:
                if not self.nullable:
                    raise ValueError(f"Field '{self.name}' is not nullable and cannot default to null")
            else:
                TypeAdapter(python_type, config=_DEFAULT_CHECK).validate_python(self.default, strict=True)
        object.__setattr__(self, "constraints", MappingProxyType(dict(self.constraints)))

    @property
    def required(self) -> bool:
        return not self.nullable and not self.has_default and self.value_generation is None


@dataclass(frozen=True, slots=True)
class Relation:
    local_field: str
    target_entity: str
    target_field: str


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
        entity_class_name(self.name)
        names = [declared.name for declared in self.fields]
        if len(set(names)) != len(names):
            raise ValueError(f"Entity '{self.name}' declares a Field name more than once")
        physical = [field_attribute_name(name) for name in names]
        if len(set(physical)) != len(physical):
            raise ValueError(f"Entity '{self.name}' declares Field names that collide once normalized")
        by_name = {declared.name: declared for declared in self.fields}
        if self.primary_key != "id" or "id" not in by_name:
            raise ValueError(f"Entity '{self.name}' must name its id Field as Primary Key")
        identity = by_name["id"]
        if identity.nullable or not identity.immutable:
            raise ValueError(f"Entity '{self.name}' must declare id as non-nullable and immutable")
        activity = by_name.get("is_active")
        if activity is None or activity.type != "boolean" or activity.nullable or activity.immutable:
            raise ValueError(f"Entity '{self.name}' must declare is_active as a non-nullable mutable boolean")
        for relation in self.relations:
            if relation.local_field not in by_name:
                raise ValueError(f"Entity '{self.name}' declares a Relation on an unknown Field")
        if len(set(self.relations)) != len(self.relations):
            raise ValueError(f"Entity '{self.name}' declares a duplicate Relation")
        for kind, groups in (("Uniqueness Constraint", self.unique_constraints), ("Index", self.indexes)):
            if len(set(groups)) != len(groups):
                raise ValueError(f"Entity '{self.name}' declares a duplicate {kind}")
            for group in groups:
                if not group or len(set(group)) != len(group) or not set(group) <= set(by_name):
                    raise ValueError(f"Entity '{self.name}' declares an invalid {kind}")
