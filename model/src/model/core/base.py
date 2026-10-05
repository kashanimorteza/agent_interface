from contextvars import ContextVar
from functools import cache
from typing import Annotated, Any, ClassVar, Self

from pydantic import ConfigDict, TypeAdapter, ValidationError
from sqlalchemy import MetaData
from sqlalchemy.orm import declared_attr, registry
from sqlmodel import SQLModel

from model.core.columns import physical_name
from model.core.declaration import Declaration, FieldDeclaration, ValueGeneration
from model.core.errors import EntityValidationError
from model.core.foundation import Foundation

_VALIDATING: ContextVar[bool] = ContextVar("validating", default=False)
_RECONSTRUCTING: ContextVar[bool] = ContextVar("reconstructing", default=False)

_METADATA = MetaData(
    naming_convention={
        "pk": "pk_%(table_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ix": "ix_%(table_name)s_%(column_0_N_name)s",
    }
)


@cache
def _fields_by_name(declaration: Declaration) -> dict[str, FieldDeclaration]:
    return {field.name: field for field in declaration.fields}


_ADAPTERS: dict[type, dict[str, TypeAdapter[Any]]] = {}


def _adapter(entity: type[Entity], name: str) -> TypeAdapter[Any]:
    adapters = _ADAPTERS.setdefault(entity, {})
    if name not in adapters:
        info = entity.model_fields[name]
        annotation = (
            Annotated[(info.annotation, *info.metadata)]
            if info.metadata
            else info.annotation
        )
        adapters[name] = TypeAdapter(annotation, config=ConfigDict(strict=True))
    return adapters[name]


def _diagnostic(
    entity: type[Entity], error: ValidationError, field: str | None = None
) -> EntityValidationError:
    declaration = entity.declaration
    sensitive = {
        item.name for item in declaration.fields if item.sensitivity is not None
    }
    parts: list[str] = []
    for item in error.errors(
        include_url=False, include_context=False, include_input=False
    ):
        path = [str(part) for part in item["loc"]]
        if field is not None:
            path.insert(0, field)
        head = path[0] if path else ""
        detail = (
            item["type"] if head in sensitive else f"{item['msg']} ({item['type']})"
        )
        parts.append(f"field '{'.'.join(path)}': {detail}")
    return EntityValidationError(f"{declaration.name}: " + "; ".join(parts))


class Entity(SQLModel, Foundation, registry=registry(metadata=_METADATA)):
    declaration: ClassVar[Declaration]

    @declared_attr  # pyright: ignore[reportArgumentType]
    def __tablename__(cls) -> str:  # pyright: ignore[reportIncompatibleVariableOverride]
        return physical_name(cls.declaration.name)

    @classmethod
    def _reconstruct(cls, values: dict[str, Any]) -> Self:
        token = _RECONSTRUCTING.set(True)
        try:
            return cls(**values)
        finally:
            _RECONSTRUCTING.reset(token)

    def __init__(self, /, **data: Any) -> None:
        if _VALIDATING.get():
            super().__init__(**data)
            return
        cls = type(self)
        fields = _fields_by_name(cls.declaration)
        unknown = sorted(set(data) - set(fields))
        if unknown:
            raise EntityValidationError(
                f"{cls.declaration.name}: unknown fields {unknown}."
            )
        if not _RECONSTRUCTING.get():
            generated = sorted(
                name
                for name, field in fields.items()
                if field.value_generation is ValueGeneration.AUTO_INCREMENT
                and data.get(name) is not None
            )
            if generated:
                raise EntityValidationError(
                    f"{cls.declaration.name}: generated fields {generated} cannot be supplied."
                )
        token = _VALIDATING.set(True)
        try:
            cls.model_validate(data, strict=True)
            super().__init__(**data)
        except ValidationError as error:
            raise _diagnostic(cls, error) from None
        finally:
            _VALIDATING.reset(token)

    def __setattr__(self, name: str, value: Any) -> None:
        cls = type(self)
        field = _fields_by_name(cls.declaration).get(name)
        if field is None or _VALIDATING.get():
            super().__setattr__(name, value)
            return
        if field.immutable:
            raise EntityValidationError(
                f"{cls.declaration.name}: field '{name}' is immutable."
            )
        try:
            validated = _adapter(cls, name).validate_python(value)
        except ValidationError as error:
            raise _diagnostic(cls, error, name) from None
        super().__setattr__(name, validated)
