from typing import TYPE_CHECKING, Annotated, Any

from pydantic import ConfigDict, TypeAdapter, ValidationError

from model.core._naming import field_attribute_name
from model.core.declaration import FieldDeclaration

if TYPE_CHECKING:
    from model.core.foundation import Foundation

_ADAPTER_CONFIG = ConfigDict(hide_input_in_errors=True)

_adapters: dict[tuple[str, str], TypeAdapter[Any]] = {}
_declared: dict[str, dict[str, FieldDeclaration]] = {}


def _key(entity: type[Foundation]) -> str:
    return f"{entity.__module__}.{entity.__qualname__}"


def adapter(entity: type[Foundation], name: str) -> TypeAdapter[Any]:
    key = (_key(entity), name)
    if key not in _adapters:
        info = entity.model_fields[name]
        annotation = Annotated[info.annotation, *info.metadata] if info.metadata else info.annotation
        _adapters[key] = TypeAdapter(annotation, config=_ADAPTER_CONFIG)
    return _adapters[key]


def declared(entity: type[Foundation]) -> dict[str, FieldDeclaration]:
    key = _key(entity)
    if key not in _declared:
        _declared[key] = {field_attribute_name(item.name): item for item in entity.declaration.fields}
    return _declared[key]


def sensitive(entity: type[Foundation]) -> frozenset[str]:
    return frozenset(name for name, item in declared(entity).items() if item.sensitivity is not None)


def retarget(error: ValidationError, name: str) -> list[Any]:
    return [
        {"type": item["type"], "loc": (name,), "input": None, "ctx": item.get("ctx", {})} for item in error.errors()
    ]


def entity_error(entity: type[Foundation], line_errors: list[Any]) -> ValidationError:
    return ValidationError.from_exception_data(entity.__name__, line_errors, hide_input=True)


def reject_widening(entity: type[Foundation], values: dict[str, Any]) -> None:
    for name, value in values.items():
        if type(value) is int and declared(entity)[name].type == "float":
            raise entity_error(entity, [{"type": "float_type", "loc": (name,), "input": None}])
