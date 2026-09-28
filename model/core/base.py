from contextvars import ContextVar
from typing import Any, Self

from sqlmodel import SQLModel

from .foundation import Foundation

_partial_init: ContextVar[bool] = ContextVar("partial_init", default=False)
_MISSING = object()


class Entity(Foundation, SQLModel):
    """Base of every Entity; enforces the Field value contract on construction."""

    model_config = {"strict": True, "extra": "forbid", "hide_input_in_errors": True}

    def __init__(self, **data: Any) -> None:
        if _partial_init.get():
            return
        previous = self.__dict__.copy()
        self.__pydantic_validator__.validate_python(data, self_instance=self)
        fields_set = self.__pydantic_fields_set__.copy()
        for name, value in {**previous, **self.__dict__}.items():
            SQLModel.__setattr__(self, name, value)
        object.__setattr__(self, "__pydantic_fields_set__", fields_set)

    def __setattr__(self, name: str, value: Any) -> None:
        if name in type(self).model_fields and not _partial_init.get():
            field = next(field for field in self.declaration.fields if field.name == name)
            if field.immutable and getattr(self, name) is not None:
                raise ValueError(f"{type(self).__name__}.{name} is immutable")
            previous = vars(self).get(name, _MISSING)
            self.__pydantic_validator__.validate_assignment(self, name, value)
            value = vars(self).pop(name)
            if previous is not _MISSING:
                vars(self)[name] = previous
        SQLModel.__setattr__(self, name, value)

    def __delattr__(self, name: str) -> None:
        if name in type(self).model_fields:
            raise ValueError(f"{type(self).__name__}.{name} cannot be deleted")
        super().__delattr__(name)

    @classmethod
    def model_validate(
        cls,
        obj: Any,
        *,
        strict: bool | None = None,
        from_attributes: bool | None = None,
        context: dict[str, Any] | None = None,
        update: dict[str, Any] | None = None,
    ) -> Self:
        token = _partial_init.set(True)
        try:
            return super().model_validate(
                obj,
                strict=strict,
                from_attributes=from_attributes,
                context=context,
                update=update,
            )
        finally:
            _partial_init.reset(token)
