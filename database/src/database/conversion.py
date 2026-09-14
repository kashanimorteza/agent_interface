"""Generic, Model-driven conversion between a Domain Definition and its storage mapping."""

from __future__ import annotations

from typing import Any

from . import credentials

REDACTED = "***protected***"


def credential_fields(model_cls: type[Any]) -> tuple[str, ...]:
    return tuple(
        name
        for name, info in model_cls.model_fields.items()
        if (info.json_schema_extra or {}).get("credential")
    )


def to_orm_kwargs(instance: Any, *, db_instance_key: str) -> dict[str, Any]:
    """Convert a Domain Definition instance into ORM constructor kwargs.

    Every credential field present is protected under its resolved at-rest treatment
    before it reaches storage.
    """
    model_cls = type(instance)
    data = instance.model_dump()
    for field in credential_fields(model_cls):
        value = data.get(field)
        if value is not None:
            data[field] = credentials.protect(
                value,
                model_name=model_cls.__name__,
                field_name=field,
                instance=db_instance_key,
            )
    return data


def from_orm_kwargs(row: Any, model_cls: type[Any]) -> dict[str, Any]:
    """Convert one storage row into Domain Definition constructor kwargs.

    Every credential field is redacted: the Database Interface never returns a usable
    credential representation, whether hashed or encrypted.
    """
    data = {name: getattr(row, name) for name in model_cls.model_fields}
    for field in credential_fields(model_cls):
        if data.get(field) is not None:
            data[field] = REDACTED
    return data
