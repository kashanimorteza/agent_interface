"""Base: the private Validation shared by every Entity."""

from collections.abc import Iterable
from contextvars import ContextVar
from typing import Any, ClassVar

from pydantic import ValidationError
from sqlmodel import SQLModel
from sqlmodel.main import SQLModelConfig, SQLModelMetaclass, finish_init

from ._storage import REGISTRY
from ._types import entity_physical_name, generate_identifier
from .declaration import Declaration, ValueGeneration

_REDACTED = "[redacted]"
_initializing: ContextVar[bool] = ContextVar("initializing", default=False)


def _redacted(detail: Any, marked: set[str]) -> Any:
    """Return one validation error detail with the input of a sensitive Field replaced."""
    if not (detail["loc"] and detail["loc"][0] in marked):
        return {
            key: detail[key] for key in ("type", "loc", "input", "ctx") if key in detail
        }
    context = {
        key: ValueError("Invalid value") if key == "error" else item
        for key, item in detail.get("ctx", {}).items()
    }
    return {
        "type": detail["type"],
        "loc": detail["loc"],
        "input": _REDACTED,
        **({"ctx": context} if context else {}),
    }


class DefinitionError(TypeError):
    """An Entity type disagrees with its Declaration."""


def _check_definition(entity: Any) -> None:
    """Fail loading when an Entity type disagrees with its Declaration."""
    declaration = getattr(entity, "declaration", None)
    if declaration is None:
        raise DefinitionError(f"{entity.__name__} declares no Declaration")
    physical = entity_physical_name(declaration.name)
    if entity.__name__ != physical:
        raise DefinitionError(
            f"{entity.__name__} must be named {physical} to match its Declaration"
        )
    if entity.__dict__.get("__tablename__") != physical:
        raise DefinitionError(
            f"{entity.__name__} must have the table name {physical} to match its Declaration"
        )
    if list(entity.model_fields) != [item.name for item in declaration.fields]:
        raise DefinitionError(
            f"{entity.__name__} must declare exactly the Fields of its Declaration, in the same order"
        )


class _EntityMetaclass(SQLModelMetaclass):
    def __init__(
        cls,
        name: str,
        bases: tuple[type, ...],
        class_dict: dict[str, Any],
        **kwargs: Any,
    ) -> None:
        if kwargs.get("table"):
            _check_definition(cls)
        super().__init__(name, bases, class_dict, **kwargs)

    def __setattr__(cls, name: str, value: Any) -> None:
        if (
            name == "declaration"
            and "declaration" in cls.__dict__
            and value is not cls.__dict__["declaration"]
        ):
            raise AttributeError("The Declaration of an Entity is read-only")
        super().__setattr__(name, value)


class Base(SQLModel, metaclass=_EntityMetaclass, registry=REGISTRY):
    """Validates every Entity strictly, on top of the selected modeling package."""

    model_config = SQLModelConfig(strict=True, extra="forbid", validate_default=True)

    declaration: ClassVar[Declaration]

    __hash__ = None  # type: ignore[assignment]  # a mutable Entity is not hashable

    def __init__(self, /, **data: Any) -> None:
        # The modeling package creates blank table instances while it validates; those skip validation here.
        if finish_init.get():
            cls = type(self)
            cls._refuse_auto_increment(data)
            data = cls._validated_values(cls._with_generated_identifiers(data))
        token = _initializing.set(True)
        try:
            super().__init__(**data)
        finally:
            _initializing.reset(token)

    def __setattr__(self, name: str, value: Any) -> None:
        cls = type(self)
        if _initializing.get() or name not in cls.model_fields:
            super().__setattr__(name, value)
            return
        field = next(item for item in cls.declaration.fields if item.name == name)
        cls._refuse_auto_increment((name,))
        if field.immutable:
            raise ValueError(f"The Field {name!r} of {cls.__name__} is immutable")
        candidate = {item: getattr(self, item) for item in cls.model_fields}
        candidate[name] = value
        validated = cls._validated_values(candidate)
        super().__setattr__(name, validated[name])

    @classmethod
    def _refuse_auto_increment(cls, names: Iterable[str]) -> None:
        """Refuse a caller-supplied value for an Auto Increment Field, which stays pending until storage assigns it."""
        declaration = getattr(cls, "declaration", None)
        if declaration is None:
            return
        for item in declaration.fields:
            if (
                item.value_generation == ValueGeneration.auto_increment
                and item.name in names
            ):
                raise ValueError(
                    f"The Auto Increment Field {item.name!r} of {cls.__name__} is assigned by storage and cannot be supplied"
                )

    @classmethod
    def _with_generated_identifiers(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Supply a fresh Generated Identifier for every declared one the caller left out."""
        declaration = getattr(cls, "declaration", None)
        if declaration is None:
            return data
        missing = {
            item.name: generate_identifier(item.type)
            for item in declaration.fields
            if item.value_generation == ValueGeneration.generated_identifier
            and item.name not in data
        }
        return {**data, **missing} if missing else data

    @classmethod
    def _validated_values(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Validate a complete set of Field values and return them with every default applied."""
        probe = cls.__new__(cls)
        try:
            cls.__pydantic_validator__.validate_python(values, self_instance=probe)
        except ValidationError as error:
            raise cls._without_sensitive_input(error) from None
        return {name: probe.__dict__[name] for name in cls.model_fields}

    @classmethod
    def _without_sensitive_input(cls, error: ValidationError) -> Exception:
        """Return the error with the input of every sensitive Field replaced, or the error itself when none is involved."""
        declaration = getattr(cls, "declaration", None)
        marked = (
            {item.name for item in declaration.fields if item.sensitivity is not None}
            if declaration
            else set()
        )
        details = error.errors()
        if not any(detail["loc"] and detail["loc"][0] in marked for detail in details):
            return error
        try:
            return ValidationError.from_exception_data(
                error.title, [_redacted(detail, marked) for detail in details]
            )
        except KeyError, TypeError, ValueError:
            names = sorted(
                {
                    str(detail["loc"][0])
                    for detail in details
                    if detail["loc"] and detail["loc"][0] in marked
                }
            )
            return ValueError(
                f"Validation failed for the sensitive Field(s) {', '.join(names)}"
            )
