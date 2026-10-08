"""Validation (private): the strict behavior every Entity shares."""

from contextvars import ContextVar
from typing import Any, ClassVar, LiteralString, Self, cast

from pydantic import ValidationError
from pydantic_core import InitErrorDetails, PydanticCustomError
from sqlmodel import SQLModel
from sqlmodel.main import SQLModelConfig, finish_init

from model.core._storage import ENTITY_REGISTRY, physical_name
from model.core.declaration import Declaration, ValueGeneration

_HIDDEN = "[hidden]"

_building: ContextVar[bool] = ContextVar("model_building", default=False)


def _mask(value: Any, sensitive: set[str]) -> Any:
    """Return value with the entries of Sensitivity-marked Fields replaced."""
    if isinstance(value, dict):
        return {
            key: _HIDDEN if key in sensitive else item for key, item in value.items()
        }
    return value


def _hide_sensitive_input(error: ValidationError, cls: type[Base]) -> ValidationError:
    """Replace every sensitive value the error would otherwise echo."""
    sensitive = {
        item.name for item in cls.declaration.fields if item.sensitivity is not None
    }
    errors = error.errors(include_url=False, include_context=False)
    details = []
    changed = False
    for item in errors:
        hidden = bool(item["loc"]) and item["loc"][0] in sensitive
        shown = _HIDDEN if hidden else _mask(item["input"], sensitive)
        changed = changed or shown != item["input"]
        details.append(
            InitErrorDetails(
                type=PydanticCustomError(
                    cast(LiteralString, item["type"]), cast(LiteralString, item["msg"])
                ),
                loc=item["loc"],
                input=shown,
            )
        )
    if not changed:
        return error
    return ValidationError.from_exception_data(error.title, details)


class Base(SQLModel, registry=ENTITY_REGISTRY):
    model_config = SQLModelConfig(
        strict=True, extra="forbid", validate_default=True, allow_inf_nan=False
    )

    declaration: ClassVar[Declaration]

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        if "declaration" not in cls.__dict__:
            return
        physical = physical_name(cls.declaration.name)
        if cls.__name__ != physical or cls.__tablename__ != physical:
            raise TypeError(
                f"Entity {cls.declaration.name!r} must have type and table named "
                f"{physical!r}, not {cls.__name__!r} and {cls.__tablename__!r}"
            )
        declared = tuple(item.name for item in cls.declaration.fields)
        if tuple(cls.model_fields) != declared:
            raise TypeError(
                f"Entity {physical!r} must declare exactly the Fields of its "
                "Declaration, in the same order"
            )

    def __init__(self, **data: Any) -> None:
        if not finish_init.get():
            super().__init__(**data)
            return
        cls = type(self)
        generated = {
            item.name
            for item in cls.declaration.fields
            if item.value_generation is ValueGeneration.auto_increment
        }
        supplied = sorted(generated & data.keys())
        if supplied:
            raise ValueError(
                f"{', '.join(supplied)}: the value is generated and cannot be supplied"
            )
        entity = cls.model_validate(data)
        token = _building.set(True)
        try:
            super().__init__(
                **{name: getattr(entity, name) for name in cls.model_fields}
            )
        finally:
            _building.reset(token)

    def __setattr__(self, name: str, value: Any) -> None:
        cls = type(self)
        if not _building.get() and name in cls.model_fields:
            spec = next(item for item in cls.declaration.fields if item.name == name)
            if (
                spec.immutable
                or spec.value_generation is ValueGeneration.auto_increment
            ):
                raise ValueError(f"{name}: the Field cannot be assigned")
            candidate = {field: getattr(self, field) for field in cls.model_fields}
            candidate[name] = value
            cls.model_validate(candidate)
        super().__setattr__(name, value)

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
        token = _building.set(True)
        try:
            return super().model_validate(
                obj,
                strict=strict,
                from_attributes=from_attributes,
                context=context,
                update=update,
            )
        except ValidationError as error:
            raise _hide_sensitive_input(error, cls) from None
        finally:
            _building.reset(token)
