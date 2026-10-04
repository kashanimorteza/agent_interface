"""Private shared base of every Entity: strict Field contracts on construction and mutation."""

from contextvars import ContextVar
from datetime import date, time
from decimal import Decimal
from types import UnionType
from typing import Annotated, Any, Self, Union, get_args, get_origin
from uuid import UUID

from pydantic import AwareDatetime, ConfigDict
from sqlmodel import SQLModel
from sqlmodel._compat import finish_init

from model.core.declaration import NO_DEFAULT, Declaration, FieldDeclaration
from model.core.foundation import Foundation

_constructing: ContextVar[bool] = ContextVar("model_entity_constructing", default=False)
_allow_generated: ContextVar[bool] = ContextVar(
    "model_entity_allow_generated", default=False
)

_ANNOTATION_TYPES: dict[str, Any] = {
    "string": str,
    "integer": int,
    "float": float,
    "decimal": Decimal,
    "boolean": bool,
    "datetime": AwareDatetime,
    "date": date,
    "time": time,
    "uuid": UUID,
}


def _base_annotation(annotation: Any) -> tuple[Any, bool]:
    """Split an annotation into its non-null type and whether it admits null."""
    admits_null = False
    if get_origin(annotation) in (Union, UnionType):
        arguments = [
            argument for argument in get_args(annotation) if argument is not type(None)
        ]
        admits_null = len(arguments) != len(get_args(annotation))
        annotation = arguments[0]
    if get_origin(annotation) is Annotated:
        annotation = get_args(annotation)[0]
    return annotation, admits_null


class Entity(Foundation, SQLModel):
    """Base of every Entity: it adds no Field and no behaviour beyond the Field contracts."""

    model_config = ConfigDict(  # pyright: ignore[reportAssignmentType]
        strict=True, extra="forbid", hide_input_in_errors=True
    )

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        declaration = cls.__dict__.get("declaration")
        if declaration is not None:
            _require_conformance(cls, declaration)

    def __init__(self, **data: Any) -> None:
        if finish_init.get() and not _constructing.get():
            cls = type(self)
            _reject_invalid_keys(cls, data)
            token = _constructing.set(True)
            try:
                cls.model_validate(data, strict=True)
                super().__init__(**data)
            finally:
                _constructing.reset(token)
        else:
            super().__init__(**data)

    @classmethod
    def _from_values(cls, values: dict[str, Any]) -> Self:
        token = _allow_generated.set(True)
        try:
            return cls(**values)
        finally:
            _allow_generated.reset(token)

    def __setattr__(self, name: str, value: Any) -> None:
        cls = type(self)
        if name in cls.model_fields and finish_init.get() and not _constructing.get():
            field = cls.declaration.field(name)
            if field.immutable or field.value_generation is not None:
                raise ValueError(f"Field '{name}' is immutable.")
            values = {
                field_name: getattr(self, field_name) for field_name in cls.model_fields
            }
            values[name] = value
            token = _constructing.set(True)
            try:
                candidate = cls.model_validate(values, strict=True)
            finally:
                _constructing.reset(token)
            super().__setattr__(name, getattr(candidate, name))
            return
        super().__setattr__(name, value)


def _reject_invalid_keys(cls: type[Entity], data: dict[str, Any]) -> None:
    unknown = sorted(set(data) - set(cls.model_fields))
    if unknown:
        raise ValueError(f"Unknown Field '{unknown[0]}'.")
    if _allow_generated.get():
        return
    for field in cls.declaration.fields:
        if (
            field.value_generation == "auto_increment"
            and data.get(field.name) is not None
        ):
            raise ValueError(
                f"Field '{field.name}' is generated and cannot be supplied."
            )


def _require_conformance(cls: type[Entity], declaration: Declaration) -> None:
    """Fail definition of an Entity whose realization differs from its own Declaration."""
    problems: list[str] = []
    if list(cls.model_fields) != [field.name for field in declaration.fields]:
        problems.append("Fields differ from the Declaration in name or order")
    else:
        for field in declaration.fields:
            problems.extend(_field_problems(cls, declaration, field))
    if problems:
        raise TypeError(
            f"Entity '{cls.__name__}' does not realize its Declaration: {'; '.join(problems)}."
        )


def _field_problems(
    cls: type[Entity], declaration: Declaration, field: FieldDeclaration
) -> list[str]:
    info = cls.model_fields[field.name]
    base, admits_null = _base_annotation(info.annotation)
    problems: list[str] = []
    if base is not _ANNOTATION_TYPES[field.type]:
        problems.append(f"Field '{field.name}' has a different type")
    if field.value_generation == "auto_increment":
        if not admits_null or info.default is not None:
            problems.append(f"Field '{field.name}' must stay pending until generated")
    else:
        if admits_null != field.nullable:
            problems.append(f"Field '{field.name}' has a different nullability")
        if field.default is NO_DEFAULT:
            if field.nullable and (info.is_required() or info.default is not None):
                problems.append(f"Field '{field.name}' must be absent-as-null")
            elif not field.nullable and not info.is_required():
                problems.append(f"Field '{field.name}' must be required")
        elif info.is_required() or info.default != field.default:
            problems.append(f"Field '{field.name}' has a different default")
    if (getattr(info, "primary_key", None) is True) != (
        field.name == declaration.primary_key
    ):
        problems.append(f"Field '{field.name}' has a different primary key role")
    expected_foreign_key = next(
        (
            f"{relation.target_entity.replace(' ', '')}.{relation.target_field}"
            for relation in declaration.relations
            if relation.local_field == field.name
        ),
        None,
    )
    actual_foreign_key = getattr(info, "foreign_key", None)
    if not isinstance(actual_foreign_key, str):
        actual_foreign_key = None
    if actual_foreign_key != expected_foreign_key:
        problems.append(f"Field '{field.name}' has a different Relation")
    expected_unique = (field.name,) in declaration.unique_constraints
    if (getattr(info, "unique", None) is True) != expected_unique:
        problems.append(f"Field '{field.name}' has a different uniqueness")
    return problems
