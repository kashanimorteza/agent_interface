"""Private Base: the Validation every Entity inherits, built on the selected modeling package."""

from collections.abc import Generator, Mapping
from contextlib import contextmanager
from contextvars import ContextVar
from types import NoneType
from typing import Annotated, Any, ClassVar, LiteralString, Self, cast

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    ValidationError,
    create_model,
)
from pydantic import Field as PydanticField
from pydantic_core import InitErrorDetails, PydanticCustomError, PydanticKnownError
from sqlmodel import SQLModel
from sqlmodel.main import finish_init

from model.core import _storage, _types
from model.core.declaration import EntityDeclaration, FieldDeclaration, ValueGeneration

_REDACTED = "[redacted]"

#: Whether the Entity itself, rather than a caller, is setting values.
_trusted: ContextVar[bool] = ContextVar("model_trusted", default=False)


@contextmanager
def _trust() -> Generator[None]:
    token = _trusted.set(True)
    try:
        yield
    finally:
        _trusted.reset(token)


class AssignmentError(ValueError):
    """Raised when a Field cannot be assigned."""


class DefinitionError(ValueError):
    """Raised when an Entity type disagrees with its Declaration."""


def _require_float(value: Any) -> Any:
    """Refuse every value that is not a float: an integer is not implicitly converted."""
    if type(value) is not float:
        raise PydanticKnownError("float_type")
    return value


def _validation_field(field: FieldDeclaration) -> tuple[Any, Any]:
    """The strict validation shape of one Field, derived only from its Field Declaration."""
    if field.value_generation is ValueGeneration.auto_increment:
        return NoneType, PydanticField(default=None)
    annotation: Any = _types.ANNOTATIONS[field.type]
    if field.type == "float":
        annotation = Annotated[float, BeforeValidator(_require_float)]
    options: dict[str, Any] = {"description": field.description}
    if field.nullable:
        annotation = annotation | None
    if field.has_default:
        options["default"] = field.default
    elif field.value_generation is ValueGeneration.generated_identifier:
        options["default_factory"] = _types.identifier_factory(field.type)
    elif field.nullable:
        options["default"] = None
    if field.constraints.size is not None:
        options["max_length"] = field.constraints.size
    if field.type == "float":
        options["allow_inf_nan"] = False
    return annotation, PydanticField(**options)


def build_validator(declaration: EntityDeclaration) -> type[BaseModel]:
    """The strict whole-Entity validator of a Declaration: declared Fields only, no coercion."""
    fields: dict[str, Any] = {f.name: _validation_field(f) for f in declaration.fields}
    return create_model(
        f"{_storage.physical_name(declaration.name)}Validation",
        __config__=ConfigDict(strict=True, extra="forbid", validate_default=True),
        **fields,
    )


def _sanitize(
    error: ValidationError, declaration: EntityDeclaration
) -> ValidationError:
    """The same validation failure with every input value that could be sensitive replaced."""
    marked = {f.name for f in declaration.fields if f.sensitivity is not None}
    known = set(declaration.field_names)
    details: list[InitErrorDetails] = []
    for detail in error.errors(include_url=False):
        loc = detail["loc"]
        field = loc[0] if loc else None
        if field in marked:
            kind = PydanticCustomError(
                cast(LiteralString, detail["type"]), cast(LiteralString, detail["msg"])
            )
            details.append(InitErrorDetails(type=kind, loc=loc, input=_REDACTED))
            continue
        shown = field in known and detail["type"] != "missing"
        entry = InitErrorDetails(
            type=detail["type"], loc=loc, input=detail["input"] if shown else _REDACTED
        )
        if "ctx" in detail:
            entry["ctx"] = detail["ctx"]
        details.append(entry)
    return ValidationError.from_exception_data(error.title, details)


class Base(SQLModel, registry=_storage.REGISTRY):
    """Shared Validation for every Entity."""

    declaration: ClassVar[EntityDeclaration]
    __entity_validator__: ClassVar[type[BaseModel]]
    __hash__ = None  # type: ignore[assignment]

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        declaration = cls.__dict__.get("declaration")
        if declaration is None:
            if cls.model_fields:
                raise DefinitionError(
                    f"{cls.__name__}: a type that defines Fields must hold its Declaration."
                )
            return
        cls._check_definition(declaration)
        cls.__entity_validator__ = build_validator(declaration)

    @classmethod
    def _check_definition(cls, declaration: EntityDeclaration) -> None:
        """Fail loading when the type disagrees with its Declaration."""
        physical = _storage.physical_name(declaration.name)
        if cls.__name__ != physical:
            raise DefinitionError(f"{cls.__name__}: the type name must be {physical}.")
        if cls.__dict__.get("__tablename__") != physical:
            raise DefinitionError(f"{cls.__name__}: the table name must be {physical}.")
        declared = list(declaration.field_names)
        actual = list(cls.model_fields)
        if actual != declared:
            raise DefinitionError(
                f"{cls.__name__}: the Fields must be exactly the Declaration's Fields in order; "
                f"declared {declared}, defined {actual}."
            )

    @classmethod
    def _validate(cls, data: dict[str, Any]) -> BaseModel:
        """Validate a whole Entity's values before any value is set."""
        try:
            return cls.__entity_validator__.model_validate(data)
        except ValidationError as error:
            failure = _sanitize(error, cls.declaration)
        # Raised outside the handler so the original message, which holds the input, is never chained.
        raise failure from None

    @classmethod
    def model_validate(cls, obj: Any, **options: Any) -> Self:
        """Build an Entity from a mapping or a model of Field values, with the rules of direct construction.

        Entities are always strict: the library's validation options are accepted and ignored,
        except `update`, which overrides values before validation.
        """
        if isinstance(obj, cls):
            return obj
        if isinstance(obj, BaseModel):
            data = obj.model_dump(exclude_unset=True)
        elif isinstance(obj, Mapping):
            data = dict(obj)
        else:
            raise TypeError(
                f"{cls.__name__} is built from a mapping or a model, not {type(obj).__name__}."
            )
        data.update(options.get("update") or {})
        return cls(**data)

    def __init__(self, **data: Any) -> None:
        if not finish_init.get():
            super().__init__(**data)
            return
        validated = self._validate(data)
        values = dict(data)
        for field in self.declaration.fields:
            if (
                field.value_generation is ValueGeneration.generated_identifier
                and field.name not in values
            ):
                values[field.name] = getattr(validated, field.name)
        with _trust():
            super().__init__(**values)

    def __setattr__(self, name: str, value: Any) -> None:
        if _trusted.get() or name.startswith("_"):
            super().__setattr__(name, value)
            return
        declaration = self.declaration
        if name not in declaration.field_names:
            raise AttributeError(f"{type(self).__name__} has no Field {name!r}.")
        field = declaration.field(name)
        if field.immutable:
            raise AssignmentError(f"Field {name} is immutable.")
        if field.value_generation is ValueGeneration.auto_increment:
            raise AssignmentError(
                f"Field {name} is assigned by storage and is closed to callers."
            )
        candidate = {
            f.name: getattr(self, f.name)
            for f in declaration.fields
            if f.value_generation is not ValueGeneration.auto_increment
        }
        candidate[name] = value
        self._validate(candidate)
        with _trust():
            super().__setattr__(name, value)
