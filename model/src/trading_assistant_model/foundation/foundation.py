"""Shared validation and JSON conversion behaviour for every Entity.

Foundation supplies behaviour only. Each Entity's meaning stays in its Declaration, and
Foundation adds no Field, constraint or domain meaning of its own.
"""

import json
import re
import types
from collections.abc import Mapping
from contextvars import ContextVar
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any, ClassVar, Self, Union, get_args, get_origin

from pydantic import AwareDatetime, ValidationError
from pydantic_core import InitErrorDetails, PydanticCustomError, PydanticUndefined
from sqlmodel import SQLModel

from ..declaration import OMITTED, Declaration, FieldDeclaration, FieldType

# True while Foundation itself is building an instance, so SQLModel's internal
# re-entrant construction does not validate again.
_building: ContextVar[bool] = ContextVar("foundation_building", default=False)

_PYTHON_TYPES: dict[Any, FieldType] = {
    int: FieldType.INTEGER,
    str: FieldType.STRING,
    bool: FieldType.BOOLEAN,
    Decimal: FieldType.DECIMAL,
    float: FieldType.FLOAT,
    AwareDatetime: FieldType.DATETIME,
}
_RESTRICTIONS = {"min", "max", "pattern", "allowed_values", "precision", "scale"}
_HIDDEN = "[hidden]"


def _split_optional(annotation: Any) -> tuple[Any, bool]:
    """Split ``T | None`` into ``T`` and whether ``None`` was allowed."""
    if get_origin(annotation) in (types.UnionType, Union):
        args = [a for a in get_args(annotation) if a is not type(None)]
        return (args[0] if len(args) == 1 else annotation), len(args) != len(
            get_args(annotation)
        )
    return annotation, False


def _same_default(actual: Any, field: FieldDeclaration) -> bool:
    """Return whether an Entity's Field default equals the Declaration's meaning."""
    if field.default is not OMITTED:
        expected = field.default
    elif field.nullable is True or field.generation is not OMITTED:
        expected = None
    else:
        expected = PydanticUndefined
    return actual is expected or (
        type(actual) is type(expected) and bool(actual == expected)
    )


class Foundation(SQLModel):
    """Base of every Entity: validates data against the Entity's Declaration.

    Attributes:
        declaration: The Entity's technology-independent meaning, supplied by each Entity.
    """

    model_config = SQLModel.model_config.copy()
    model_config["strict"] = True
    model_config["extra"] = "ignore"

    declaration: ClassVar[Declaration]

    def __init__(self, **data: Any) -> None:
        if _building.get():
            super().__init__()
            return
        values = self._checked(data)
        token = _building.set(True)
        try:
            super().__init__(**values)
        finally:
            _building.reset(token)

    def __setattr__(self, name: str, value: Any) -> None:
        cls = type(self)
        if _building.get() or name not in cls.model_fields:
            super().__setattr__(name, value)
            return
        field = next(f for f in cls.declaration.fields if f.name == name)
        if field.immutable is True:
            raise ValidationError.from_exception_data(
                cls.__name__,
                [
                    InitErrorDetails(
                        type="frozen_field",
                        loc=(name,),
                        input=_HIDDEN if field.sensitive is True else value,
                    )
                ],
            )
        current = {f.name: getattr(self, f.name) for f in cls.declaration.fields}
        checked = cls._validated({**current, name: value})
        super().__setattr__(name, getattr(checked, name))

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        if "declaration" in vars(cls):
            cls._verify_declaration()

    @classmethod
    def _verify_declaration(cls) -> None:
        """Fail at class definition when the Entity's fields disagree with its Declaration."""
        declared = cls.declaration
        if [f.name for f in declared.fields] != list(cls.model_fields):
            raise TypeError(f"{cls.__name__}: fields differ from its Declaration")
        for field in declared.fields:
            info = cls.model_fields[field.name]
            base, allows_none = _split_optional(info.annotation)
            if _PYTHON_TYPES.get(base) is not field.type:
                raise TypeError(
                    f"{cls.__name__}.{field.name}: type differs from its Declaration"
                )
            if allows_none != (
                field.nullable is True or field.generation is not OMITTED
            ):
                raise TypeError(
                    f"{cls.__name__}.{field.name}: nullability differs from its Declaration"
                )
            unknown = set(field.restrictions) - _RESTRICTIONS
            if unknown:
                raise TypeError(
                    f"{cls.__name__}.{field.name}: unsupported restriction {sorted(unknown)}"
                )
            if not _same_default(info.get_default(call_default_factory=False), field):
                raise TypeError(
                    f"{cls.__name__}.{field.name}: default differs from its Declaration"
                )
            max_length = next(
                (m.max_length for m in info.metadata if hasattr(m, "max_length")),
                OMITTED,
            )
            if max_length != field.length:
                raise TypeError(
                    f"{cls.__name__}.{field.name}: length differs from its Declaration"
                )

    @classmethod
    def _validated(cls, data: Mapping[str, Any]) -> Self:
        """Validate ``data`` against the Declaration and return the checked instance."""
        token = _building.set(True)
        try:
            validated = cls.model_validate(dict(data))
            problems = cls._restriction_problems(validated)
            if not problems:
                return validated
            failure = ValidationError.from_exception_data(cls.__name__, problems)
        except ValidationError as error:
            failure = cls._redacted(error)
        finally:
            _building.reset(token)
        raise failure

    @classmethod
    def _redacted(cls, error: ValidationError) -> ValidationError:
        """Rebuild a validation failure so no sensitive input value appears in it."""
        sensitive = {f.name for f in cls.declaration.fields if f.sensitive is True}
        details: list[InitErrorDetails] = []
        for item in error.errors(include_url=False):
            value = item["input"]
            if item["loc"] and item["loc"][0] in sensitive:
                value = _HIDDEN
            elif isinstance(value, Mapping):
                value = {k: _HIDDEN if k in sensitive else v for k, v in value.items()}
            detail = InitErrorDetails(type=item["type"], loc=item["loc"], input=value)
            if "ctx" in item:
                detail["ctx"] = item["ctx"]
            details.append(detail)
        return ValidationError.from_exception_data(error.title, details)

    @classmethod
    def _checked(cls, data: Mapping[str, Any]) -> dict[str, Any]:
        """Return the checked values of the Fields that ``data`` supplied."""
        validated = cls._validated(data)
        return {name: getattr(validated, name) for name in validated.model_fields_set}

    @classmethod
    def from_json(cls, data: str | bytes | Mapping[str, Any]) -> Self:
        """Create a validated instance from JSON.

        Follows exactly the same rules as direct construction, after reading JSON's
        string forms of exact decimals and date-times.

        Args:
            data (str | bytes | Mapping): JSON text, or an already parsed JSON object.

        Returns:
            (Self): The validated instance.
        """
        problem = None
        parsed: Any = data
        if isinstance(data, str | bytes):
            try:
                parsed = json.loads(data)
            except ValueError as error:
                problem = f"Invalid JSON ({type(error).__name__})"
        if problem is None and not isinstance(parsed, Mapping):
            problem = "JSON must be an object"
        if problem is not None:
            raise ValueError(problem)
        return cls(
            **{name: cls._decoded(name, value) for name, value in parsed.items()}
        )

    @classmethod
    def _decoded(cls, name: str, value: Any) -> Any:
        """Read JSON's string form of an exact decimal or date-time; leave anything else as given."""
        field = next((f for f in cls.declaration.fields if f.name == name), None)
        try:
            if field is None:
                return value
            if field.type is FieldType.DECIMAL and (
                isinstance(value, str)
                or (isinstance(value, int) and not isinstance(value, bool))
            ):
                return Decimal(value)
            if field.type is FieldType.DATETIME and isinstance(value, str):
                return datetime.fromisoformat(value)
            if (
                field.type is FieldType.FLOAT
                and isinstance(value, int)
                and not isinstance(value, bool)
            ):
                return float(value)
        except InvalidOperation, ValueError:
            pass
        return value

    def to_json(self) -> str:
        """Convert this instance to JSON text after verifying it against its Declaration.

        Returns:
            (str): A JSON object holding every declared Field; exact decimals and
                date-times are written as strings.
        """
        current = {f.name: getattr(self, f.name) for f in self.declaration.fields}
        return json.dumps(type(self)._validated(current).model_dump(mode="json"))

    @classmethod
    def _restriction_problems(cls, instance: Foundation) -> list[InitErrorDetails]:
        """Check every declared restriction of every Field that holds a value."""
        problems: list[InitErrorDetails] = []
        for field in cls.declaration.fields:
            value = getattr(instance, field.name)
            if value is None:
                continue
            for name, limit in field.restrictions.items():
                if not _satisfies(name, limit, value):
                    problems.append(
                        InitErrorDetails(
                            type=PydanticCustomError(
                                "declared_restriction",
                                "Violates declared restriction '{name}'",
                                {"name": name},
                            ),
                            loc=(field.name,),
                            input=_HIDDEN if field.sensitive is True else value,
                        )
                    )
        return problems


def _satisfies(name: str, limit: Any, value: Any) -> bool:
    """Return whether ``value`` meets one declared restriction."""
    match name:
        case "min":
            return value >= limit
        case "max":
            return value <= limit
        case "pattern":
            return re.fullmatch(limit, value) is not None
        case "allowed_values":
            return value in limit
        case "precision":
            return len(Decimal(value).as_tuple().digits) <= limit
        case "scale":
            exponent = Decimal(value).as_tuple().exponent
            return isinstance(exponent, int) and -exponent <= limit
    raise AssertionError(name)
