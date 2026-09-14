"""Transport-only schemas derived from Model, created only where shape differs from Model
itself (task P3-G10-T1). Credential fields are excluded from every output schema —
Backend Principle 11 requires their value never cross the API boundary in a response.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, create_model

from ..model_interface import ModelBase

_create_cache: dict[type[ModelBase], type[BaseModel]] = {}
_update_cache: dict[type[ModelBase], type[BaseModel]] = {}
_output_cache: dict[type[ModelBase], type[BaseModel]] = {}


def credential_fields(model_cls: type[ModelBase]) -> tuple[str, ...]:
    result: list[str] = []
    for name, info in model_cls.model_fields.items():
        extra = info.json_schema_extra
        if isinstance(extra, dict) and extra.get("credential"):
            result.append(name)
    return tuple(result)


def _annotation(info: Any) -> Any:
    assert info.annotation is not None
    return info.annotation


def create_schema_for(model_cls: type[ModelBase]) -> type[BaseModel]:
    if model_cls not in _create_cache:
        fields: dict[str, Any] = {}
        for name, info in model_cls.model_fields.items():
            if name == "id":
                continue
            default = Field() if info.is_required() else Field(default=info.default)
            fields[name] = (_annotation(info), default)
        _create_cache[model_cls] = create_model(f"{model_cls.__name__}Create", **fields)
    return _create_cache[model_cls]


def update_schema_for(model_cls: type[ModelBase]) -> type[BaseModel]:
    if model_cls not in _update_cache:
        fields: dict[str, Any] = {}
        for name, info in model_cls.model_fields.items():
            if name == "id":
                continue
            fields[name] = (_annotation(info) | None, Field(default=None))
        _update_cache[model_cls] = create_model(f"{model_cls.__name__}Update", **fields)
    return _update_cache[model_cls]


def output_schema_for(model_cls: type[ModelBase]) -> type[BaseModel]:
    if model_cls not in _output_cache:
        excluded = set(credential_fields(model_cls))
        fields: dict[str, Any] = {}
        for name, info in model_cls.model_fields.items():
            if name in excluded:
                continue
            default = Field() if info.is_required() else Field(default=info.default)
            fields[name] = (_annotation(info), default)
        _output_cache[model_cls] = create_model(f"{model_cls.__name__}Read", **fields)
    return _output_cache[model_cls]
