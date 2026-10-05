from collections.abc import Sequence
from typing import Any
from uuid import uuid4

from pydantic import ValidationError
from sqlalchemy.orm import declared_attr
from sqlmodel import SQLModel
from sqlmodel._compat import SQLModelConfig, finish_init

from model.core._fields import adapter, declared, entity_error, reject_widening, retarget, sensitive
from model.core._naming import entity_class_name, field_attribute_name
from model.core._types import realize
from model.core.foundation import Foundation

_MISSING = object()

SQLModel.metadata.naming_convention = {
    "pk": "pk_%(table_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ix": "ix_%(table_name)s_%(column_0_N_name)s",
}


class EntityBase(Foundation, SQLModel):
    model_config = SQLModelConfig(strict=True, extra="forbid", hide_input_in_errors=True)

    @declared_attr  # pyright: ignore[reportArgumentType]
    def __tablename__(cls) -> str:  # pyright: ignore[reportIncompatibleVariableOverride]
        return cls.__name__

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        declaration = cls.__dict__.get("declaration")
        if declaration is None:
            return
        if cls.__name__ != entity_class_name(declaration.name):
            raise TypeError(f"Entity '{declaration.name}' must be realized under its normalized class name")
        expected_names = [field_attribute_name(item.name) for item in declaration.fields]
        if list(cls.model_fields) != expected_names:
            raise TypeError(f"Entity '{declaration.name}' must realize exactly its declared Fields, in order")
        for item in declaration.fields:
            info = cls.model_fields[field_attribute_name(item.name)]
            expected = realize(item.type)
            if item.nullable or item.value_generation == "auto_increment":
                expected = expected | None
            if info.annotation != expected:
                raise TypeError(f"Field '{item.name}' of '{declaration.name}' is not realized as its declared Type")
            if item.required != info.is_required():
                raise TypeError(f"Field '{item.name}' of '{declaration.name}' does not realize its presence meaning")
            if item.has_default and info.default_factory is None and info.default != item.default:
                raise TypeError(f"Field '{item.name}' of '{declaration.name}' does not realize its Default Value")

    def __init__(self, **data: Any) -> None:
        if finish_init.get():
            for name, rule in declared(type(self)).items():
                if rule.value_generation == "auto_increment" and data.get(name) is not None:
                    raise ValueError(f"Field '{name}' is generated and cannot be supplied")
                if rule.value_generation == "generated_identifier" and name not in data:
                    data[name] = uuid4()
            type(self).model_validate(data, strict=True)
            reject_widening(type(self), data)
        super().__init__(**data)

    def __repr_args__(self) -> Sequence[tuple[str | None, Any]]:
        hidden = sensitive(type(self))
        return [(name, value) for name, value in super().__repr_args__() if name not in hidden]

    def __setattr__(self, name: str, value: Any) -> None:
        if name in type(self).model_fields:
            current = self.__dict__.get(name, _MISSING)
            if current is not _MISSING and not (type(value) is type(current) and value == current):
                rule = declared(type(self))[name]
                if rule.immutable or rule.value_generation == "auto_increment":
                    raise ValueError(f"Field '{name}' cannot be assigned")
                try:
                    adapter(type(self), name).validate_python(value, strict=True)
                    reject_widening(type(self), {name: value})
                except ValidationError as error:
                    raise entity_error(type(self), retarget(error, name)) from None
        super().__setattr__(name, value)
