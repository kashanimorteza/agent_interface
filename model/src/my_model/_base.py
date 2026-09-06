"""The shared base class from which every logical Model derives."""

from dataclasses import replace
from typing import Any, ClassVar, Mapping

from pydantic import BaseModel, ConfigDict

from ._spec import FieldSpec, ModelSpec, RelationshipSpec, RuleSpec


class Model(BaseModel):
    """Base of every shared logical Model.

    A Model validates its field types, nullability, and defaults on construction.
    Each subclass declares its fields as ``Annotated[<type>, FieldSpec(...)]`` and
    carries the rest of its logical definition in the ``logical_*`` attributes.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        from_attributes=True,
    )

    logical_key: ClassVar[str]
    logical_purpose: ClassVar[str]
    logical_relationships: ClassVar[tuple[RelationshipSpec, ...]] = ()
    logical_rules: ClassVar[tuple[RuleSpec, ...]] = ()
    logical_initial_data: ClassVar[tuple[Mapping[str, Any], ...]] = ()


def field_specs(model: type[Model]) -> tuple[FieldSpec, ...]:
    """Collect the field definitions of a Model in declaration order."""
    specs: list[FieldSpec] = []
    for name, info in model.model_fields.items():
        declared = [item for item in info.metadata if isinstance(item, FieldSpec)]
        if len(declared) != 1:
            raise TypeError(
                f"{model.__name__}.{name} must carry exactly one FieldSpec, found {len(declared)}"
            )
        specs.append(replace(declared[0], name=name))
    return tuple(specs)


def build_spec(model: type[Model]) -> ModelSpec:
    """Assemble the complete logical definition of a Model."""
    return ModelSpec(
        key=model.logical_key,
        purpose=model.logical_purpose,
        fields=field_specs(model),
        relationships=model.logical_relationships,
        rules=model.logical_rules,
        initial_data=model.logical_initial_data,
    )
