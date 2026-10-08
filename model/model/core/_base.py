"""Private shared Entity behaviour: Validation, Identity, and the load-time match with the Declaration."""

import keyword
from collections.abc import Mapping
from contextvars import ContextVar
from decimal import Decimal
from typing import Any, ClassVar, Self
from uuid import uuid4

from pydantic import (
    BaseModel,
    ConfigDict,
    ValidationError,
    create_model,
    field_validator,
)
from sqlalchemy import MetaData
from sqlalchemy.orm import registry
from sqlmodel import SQLModel
from sqlmodel.main import SQLModelConfig, finish_init

from model.core import _types
from model.core.declaration import (
    Declaration,
    DeclarationError,
    FieldDeclaration,
    FieldType,
    ValueGeneration,
    conforms,
)

_REDACTED = "<redacted>"

_registry = registry(metadata=MetaData())
_validators: dict[type, type[BaseModel]] = {}
_constructing: ContextVar[bool] = ContextVar("model_constructing", default=False)


def physical_name(logical_name: str) -> str:
    """Return the deterministic PascalCase physical name of an Entity's logical name."""
    words = logical_name.split()
    name = "".join(word[0].upper() + word[1:] for word in words)
    if not name.isidentifier() or keyword.iskeyword(name):
        raise DeclarationError(
            f"The Entity name '{logical_name}' has no valid physical name."
        )
    return name


def _field_declaration(cls: type[Base], name: str) -> FieldDeclaration:
    return next(field for field in cls.declaration.fields if field.name == name)


def _check_entity(cls: type[Base]) -> None:
    """Fail loading when an Entity type does not match its Declaration."""
    declaration = cls.declaration
    if not isinstance(declaration, Declaration):
        raise DeclarationError(f"{cls.__name__} must hold a Declaration.")
    expected = physical_name(declaration.name)
    if cls.__name__ != expected:
        raise DeclarationError(f"The type {cls.__name__} must be named {expected}.")
    if cls.__dict__.get("__tablename__") != expected:
        raise DeclarationError(f"The table of {cls.__name__} must be named {expected}.")
    if expected in _registry.metadata.tables:
        raise DeclarationError(
            f"Another Entity already uses the physical name {expected}."
        )
    declared = tuple(field.name for field in declaration.fields)
    if tuple(cls.model_fields) != declared:
        raise DeclarationError(
            f"The Fields of {cls.__name__} must be exactly its Declaration's Fields in order."
        )
    for field in declaration.fields:
        if (
            field.name.startswith("_")
            or keyword.iskeyword(field.name)
            or hasattr(Base, field.name)
        ):
            raise DeclarationError(
                f"The Field name '{field.name}' of {cls.__name__} cannot be used."
            )
        pending = field.value_generation is ValueGeneration.auto_increment
        if cls.model_fields[field.name].annotation != _types.annotation(
            field.type, field.nullable or pending
        ):
            raise DeclarationError(
                f"The Field '{field.name}' of {cls.__name__} does not match its Declared Type."
            )


def _require_finite(value: Any) -> Any:
    if value is not None and not conforms(
        FieldType.decimal if isinstance(value, Decimal) else FieldType.float, value
    ):
        raise ValueError("The value must be finite.")
    return value


def _refuse_integer(value: Any) -> Any:
    if isinstance(value, int):
        # Only a ValueError becomes a validation error in the validator model.
        raise ValueError("The value must be a float, not an integer.")  # noqa: TRY004
    return value


def _validator_for(cls: type[Base]) -> type[BaseModel]:
    fields: dict[str, Any] = {
        name: (info.annotation, info) for name, info in cls.model_fields.items()
    }
    finite = [
        field.name
        for field in cls.declaration.fields
        if field.type in (FieldType.float, FieldType.decimal)
    ]
    floats = [
        field.name for field in cls.declaration.fields if field.type is FieldType.float
    ]
    checks: dict[str, Any] = {}
    if finite:
        checks["finite"] = field_validator(*finite)(_require_finite)
    if floats:
        checks["not_integer"] = field_validator(*floats, mode="before")(_refuse_integer)
    config = ConfigDict(strict=True, extra="forbid", validate_default=True)
    return create_model(
        f"{cls.__name__}Validation", __config__=config, __validators__=checks, **fields
    )


def _mask(value: Any, location: tuple[Any, ...], marked: set[str]) -> Any:
    if location and location[0] in marked:
        return _REDACTED
    if isinstance(value, Mapping):
        return {
            key: _REDACTED if key in marked else item for key, item in value.items()
        }
    return value


def _sanitized(cls: type[Base], error: ValidationError) -> ValidationError:
    """Rebuild a validation error so that no input of a Sensitivity-marked Field is exposed."""
    marked = {
        field.name for field in cls.declaration.fields if field.sensitivity is not None
    }
    lines: list[Any] = []
    for item in error.errors(include_url=False):
        line: dict[str, Any] = {
            "type": item["type"],
            "loc": item["loc"],
            "input": _mask(item["input"], item["loc"], marked),
        }
        if "ctx" in item:
            line["ctx"] = item["ctx"]
        lines.append(line)
    return ValidationError.from_exception_data(cls.__name__, lines)


def _validate(cls: type[Base], values: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the whole Entity strictly and return its checked Field values."""
    failure: ValidationError | None = None
    try:
        checked = _validators[cls].model_validate(dict(values))
    except ValidationError as error:
        failure = _sanitized(cls, error)
    if failure is not None:
        raise failure
    return {name: getattr(checked, name) for name in cls.model_fields}


class Base(SQLModel):
    """The private base every Entity shares: strict, whole-Entity validation on top of the modeling package."""

    _sa_registry = _registry
    metadata = _registry.metadata
    model_config = SQLModelConfig(strict=True, extra="forbid", validate_default=True)

    declaration: ClassVar[Declaration]

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        if "declaration" in cls.__dict__:
            _check_entity(cls)
            _validators[cls] = _validator_for(cls)

    def __init__(self, **data: Any) -> None:
        cls = type(self)
        if cls not in _validators or not finish_init.get():
            super().__init__(**data)
            return
        values = dict(data)
        for field in cls.declaration.fields:
            if (
                field.value_generation is ValueGeneration.auto_increment
                and field.name in values
            ):
                raise ValueError(
                    f"The Field '{field.name}' is generated by storage and cannot be supplied."
                )
            if (
                field.value_generation is ValueGeneration.generated_identifier
                and field.name not in values
            ):
                values[field.name] = (
                    uuid4() if field.type is FieldType.uuid else str(uuid4())
                )
        checked = _validate(cls, values)
        for field in cls.declaration.fields:
            if (
                field.value_generation is ValueGeneration.auto_increment
                and checked[field.name] is None
            ):
                del checked[field.name]
        token = _constructing.set(True)
        try:
            super().__init__(**checked)
        finally:
            _constructing.reset(token)

    def __setattr__(self, name: str, value: Any) -> None:
        cls = type(self)
        if cls in _validators and name in cls.model_fields and not _constructing.get():
            field = _field_declaration(cls, name)
            if (
                field.immutable
                or field.value_generation is ValueGeneration.auto_increment
            ):
                raise ValueError(f"The Field '{name}' cannot be assigned.")
            current = {
                field_name: getattr(self, field_name) for field_name in cls.model_fields
            }
            current[name] = value
            value = _validate(cls, current)[name]
        super().__setattr__(name, value)

    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return NotImplemented
        return all(
            getattr(self, name) == getattr(other, name)
            for name in type(self).model_fields
        )

    @classmethod
    def model_validate(cls, obj: Any, **kwargs: Any) -> Self:
        if not isinstance(obj, Mapping):
            raise TypeError(
                "An Entity is validated only from a mapping of its Field values."
            )
        return cls(**obj)
