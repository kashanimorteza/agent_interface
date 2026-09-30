"""Private shared base of every Entity.

The base enforces every declared Field contract identically on construction and on
assignment, and checks at class creation that an Entity's Declaration and its
annotated Fields describe the same Fields.
"""

from collections.abc import Mapping
from contextvars import ContextVar
from datetime import datetime
from decimal import Decimal
from types import NoneType, UnionType
from typing import Annotated, Any, ClassVar, Self, Union, cast, get_args, get_origin

from pydantic import (
    AwareDatetime,
    ModelWrapValidatorHandler,
    ValidationError,
    model_validator,
)
from pydantic.config import ExtraValues
from pydantic_core import PydanticCustomError

from model.core._failure import reject, withhold_inputs
from model.core.declaration import Declaration as EntityDeclaration
from model.core.declaration import FieldDeclaration
from model.core.foundation import Foundation

_PYTHON_TYPES: dict[str, type] = {
    "integer": int,
    "string": str,
    "boolean": bool,
    "float": float,
    "decimal": Decimal,
    "datetime": datetime,
}

_assigning: ContextVar[bool] = ContextVar("model_entity_assigning", default=False)


def _annotation_types(annotation: Any) -> tuple[set[Any], bool]:
    """Flatten an annotation into its value types and whether it admits None."""
    origin = get_origin(annotation)
    if origin is Annotated:
        return _annotation_types(get_args(annotation)[0])
    if origin is Union or origin is UnionType:
        found: set[Any] = set()
        admits_none = False
        for member in get_args(annotation):
            member_types, member_none = _annotation_types(member)
            found |= member_types
            admits_none = admits_none or member_none
        return found, admits_none
    if annotation is NoneType:
        return set(), True
    return {datetime if annotation is AwareDatetime else annotation}, False


def _is_supplied(data: Any, name: str) -> bool:
    """Whether raw validation input, a mapping or an object, carries the named value."""
    if isinstance(data, Mapping):
        return name in cast(Mapping[str, Any], data)
    return hasattr(data, name)


class Entity(Foundation):
    """Flat, storage-independent base for every Entity."""

    model_config = {
        "strict": True,
        "extra": "forbid",
        "validate_assignment": True,
        "hide_input_in_errors": True,
    }

    _declared: ClassVar[dict[str, FieldDeclaration]]

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        declaration = cls.__dict__.get("Declaration")
        if declaration is None:
            return
        cls._declared = {declared.name: declared for declared in declaration.fields}
        cls._verify_declaration(declaration)

    @classmethod
    def _verify_declaration(cls, declaration: EntityDeclaration) -> None:
        fields = cls.model_fields
        if list(fields) != [declared.name for declared in declaration.fields]:
            raise TypeError(f"{declaration.name}: Fields differ from its Declaration.")
        for declared in declaration.fields:
            info = fields[declared.name]
            generated = declared.value_generation is not None
            found, admits_none = _annotation_types(info.annotation)
            problems: list[str] = []
            if found != {_PYTHON_TYPES[declared.type]}:
                problems.append("type")
            if admits_none != (declared.nullable or generated):
                problems.append("nullability")
            if info.is_required() != (
                not (declared.nullable or declared.has_default or generated)
            ):
                problems.append("presence")
            if declared.has_default and not (
                info.default == declared.default
                and type(info.default) is type(declared.default)
            ):
                problems.append("default")
            if (
                not declared.has_default
                and not info.is_required()
                and info.default is not None
            ):
                problems.append("implicit default")
            for key, value in declared.constraints.items():
                sized = [
                    getattr(item, "min_length", None) for item in info.metadata
                ] + [getattr(item, "max_length", None) for item in info.metadata]
                if key != "size" or sized.count(value) != 2:
                    problems.append(f"constraint {key}")
            if problems:
                raise TypeError(
                    f"{declaration.name}.{declared.name}: differs from its Declaration "
                    f"({', '.join(problems)})."
                )

    @model_validator(mode="before")
    @classmethod
    def _refuse_generated_values(cls, data: Any) -> Any:
        if _assigning.get() or isinstance(data, cls):
            return data
        declared: Mapping[str, FieldDeclaration] = getattr(cls, "_declared", {})
        for name, field in declared.items():
            if field.value_generation is not None and _is_supplied(data, name):
                raise PydanticCustomError(
                    "generated_value",
                    "Field {field} is generated and cannot be supplied.",
                    {"field": name},
                )
        return data

    @model_validator(mode="wrap")
    @classmethod
    def _withhold_inputs(
        cls, data: Any, handler: ModelWrapValidatorHandler[Self]
    ) -> Self:
        """Outermost validator: no failure carries a caller-supplied value."""
        try:
            return handler(data)
        except ValidationError as error:
            raise withhold_inputs(error) from None

    @classmethod
    def model_validate_json(
        cls,
        json_data: str | bytes | bytearray,
        *,
        strict: bool | None = None,
        extra: ExtraValues | None = None,
        context: Any | None = None,
        by_alias: bool | None = None,
        by_name: bool | None = None,
    ) -> Self:
        """Validate JSON text; even unparsable text withholds its input on failure."""
        try:
            return super().model_validate_json(
                json_data,
                strict=strict,
                extra=extra,
                context=context,
                by_alias=by_alias,
                by_name=by_name,
            )
        except ValidationError as error:
            failure = withhold_inputs(error)
        raise failure

    @classmethod
    def model_validate_strings(
        cls,
        obj: Any,
        *,
        strict: bool | None = None,
        extra: ExtraValues | None = None,
        context: Any | None = None,
        by_alias: bool | None = None,
        by_name: bool | None = None,
    ) -> Self:
        """Validate string-valued input; a failure withholds its input."""
        try:
            return super().model_validate_strings(
                obj,
                strict=strict,
                extra=extra,
                context=context,
                by_alias=by_alias,
                by_name=by_name,
            )
        except ValidationError as error:
            failure = withhold_inputs(error)
        raise failure

    def model_copy(
        self, *, update: Mapping[str, Any] | None = None, deep: bool = False
    ) -> Self:
        """Copy the Entity; every updated value goes through assignment enforcement."""
        duplicate = super().model_copy(deep=deep)
        for name, value in (update or {}).items():
            setattr(duplicate, name, value)
        return duplicate

    def copy(
        self,
        *,
        include: Any = None,
        exclude: Any = None,
        update: Mapping[str, Any] | None = None,
        deep: bool = False,
    ) -> Self:
        """Deprecated pydantic spelling of ``model_copy``, held to the same rules."""
        if include is not None or exclude is not None:
            raise reject(
                self.Declaration.name,
                None,
                "unsupported_copy",
                "An Entity copy always includes every Field.",
            )
        return self.model_copy(update=update, deep=deep)

    def __delattr__(self, name: str) -> None:
        if name in self._declared:
            raise reject(
                self.Declaration.name,
                name,
                "field_required",
                "Field cannot be deleted.",
            )
        super().__delattr__(name)

    def __setattr__(self, name: str, value: Any) -> None:
        declared = self._declared.get(name)
        if declared is not None:
            generated = declared.value_generation is not None
            pending = generated and getattr(self, name) is None
            if declared.immutable and not pending:
                raise reject(
                    self.Declaration.name,
                    name,
                    "immutable_field",
                    "Field cannot be changed.",
                )
            if generated and value is None:
                raise reject(
                    self.Declaration.name,
                    name,
                    "generated_field",
                    "Field cannot be reset.",
                )
        token = _assigning.set(True)
        try:
            super().__setattr__(name, value)
        finally:
            _assigning.reset(token)
