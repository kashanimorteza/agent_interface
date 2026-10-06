"""Private shared base of every Entity: strict, uniform runtime behaviour.

Table models skip validation when they are constructed, so the base validates every direct
construction itself, and rejects anything the Entity's Fields do not allow.
"""

from contextvars import ContextVar
from typing import Any, ClassVar

from pydantic import ConfigDict, ValidationError
from sqlmodel import SQLModel

from model.core._storage import physical_name
from model.core.declaration import Declaration, ValueGeneration

# True while the base is validating or populating an instance itself, so that the nested
# construction and attribute writes performed by SQLModel are not validated a second time.
_INTERNAL: ContextVar[bool] = ContextVar("model_internal", default=False)


def _redact(error: ValidationError, declaration: Declaration) -> ValidationError:
    """Return the error with the input of every sensitive Field replaced, or the error itself."""
    sensitive = {field.name for field in declaration.fields if field.sensitivity is not None}
    details: list[Any] = []
    hidden = False
    for item in error.errors(include_url=False):
        hide = bool(item["loc"]) and item["loc"][0] in sensitive
        hidden = hidden or hide
        details.append(
            {
                "type": item["type"],
                "loc": item["loc"],
                "input": "[redacted]" if hide else item["input"],
                "ctx": item.get("ctx", {}),
            }
        )
    if not hidden:
        return error
    return ValidationError.from_exception_data(error.title, details)


class Base(SQLModel):
    """Strict base: only declared Fields, no coercion, defaults that satisfy their own contract."""

    model_config = ConfigDict(  # pyright: ignore[reportAssignmentType]
        strict=True, extra="forbid", validate_default=True
    )

    declaration: ClassVar[Declaration]

    # Mutable Entities are not hashable.
    __hash__ = None  # pyright: ignore[reportAssignmentType]

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        if "declaration" not in cls.__dict__:
            return  # a shared base, not an Entity
        declaration = cls.declaration
        if cls.__name__ != physical_name(declaration.name):
            raise ValueError(f"{cls.__name__}: the class name is not the physical Entity name")
        if cls.__dict__.get("__tablename__") != cls.__name__:
            raise ValueError(f"{cls.__name__}: the table name is not the physical Entity name")
        if list(cls.model_fields) != [field.name for field in declaration.fields]:
            raise ValueError(f"{cls.__name__}: the Fields do not match its Declaration")

    def __init__(self, /, **data: Any) -> None:
        if _INTERNAL.get():
            super().__init__(**data)
            return
        cls = type(self)
        for field in cls.declaration.fields:
            # A generated Field stays pending (None) unless storage assigns it; Model never does.
            if field.value_generation is ValueGeneration.auto_increment and (
                data.get(field.name) is not None
            ):
                raise ValueError(f"{cls.declaration.name}.{field.name} is generated")
        token = _INTERNAL.set(True)
        try:
            validated = cls.model_validate(data)
            values = {name: getattr(validated, name) for name in cls.model_fields}
            super().__init__(**values)
        finally:
            _INTERNAL.reset(token)

    @classmethod
    def model_validate(  # pyright: ignore[reportIncompatibleMethodOverride]
        cls,
        obj: Any,
        *,
        strict: bool | None = None,
        from_attributes: bool | None = None,
        context: dict[str, Any] | None = None,
        update: dict[str, Any] | None = None,
    ):
        token = _INTERNAL.set(True)
        try:
            return super().model_validate(
                obj,
                strict=strict,
                from_attributes=from_attributes,
                context=context,
                update=update,
            )
        except ValidationError as error:
            redacted = _redact(error, cls.declaration)
            if redacted is error:
                raise
            failure = redacted
        finally:
            _INTERNAL.reset(token)
        # Raised outside the handler so the original error, which holds the values, is not chained.
        raise failure

    def __setattr__(self, name: str, value: Any) -> None:
        cls = type(self)
        if _INTERNAL.get() or name not in cls.model_fields:
            super().__setattr__(name, value)
            return
        for field in cls.declaration.fields:
            if field.name == name and field.immutable:
                raise ValueError(f"{cls.declaration.name}.{name} is immutable")
            if field.name == name and field.value_generation is ValueGeneration.auto_increment:
                raise ValueError(f"{cls.declaration.name}.{name} is generated")
        # Validate the whole Entity with the new value before touching the instance, so a failed
        # assignment leaves the prior value in place.
        candidate = {field: getattr(self, field) for field in cls.model_fields}
        candidate[name] = value
        validated = cls.model_validate(candidate)
        super().__setattr__(name, getattr(validated, name))
