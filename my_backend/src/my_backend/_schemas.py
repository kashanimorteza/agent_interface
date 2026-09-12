"""Generic API-schema factory: Read/Create/Update transport contracts.

These are transport contracts owned by API Interface, never the shared
domain Model and never a persistence Model — built once per Model type from
its own declared fields, so the domain definition is never copied or
duplicated by hand. A field the Model marks as a credential is write-only:
present in Create/Update, absent from Read.
"""

from __future__ import annotations

from typing import Any

from my_model._base import BaseModel as DomainModel
from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, create_model
from pydantic_core import PydanticUndefined


def _credential_fields(model_cls: type[DomainModel]) -> set[str]:
    schema = model_cls.model_json_schema()
    return {
        name
        for name, spec in schema.get("properties", {}).items()
        if spec.get("credential") is True
    }


def build_schemas(
    model_cls: type[DomainModel],
) -> tuple[type[PydanticBaseModel], type[PydanticBaseModel], type[PydanticBaseModel]]:
    """Return (Read, Create, Update) schema classes for one domain Model type."""
    name = model_cls.__name__
    credential_fields = _credential_fields(model_cls)

    read_fields: dict[str, Any] = {}
    create_fields: dict[str, Any] = {}
    update_fields: dict[str, Any] = {}

    for field_name, field_info in model_cls.model_fields.items():
        assert field_info.annotation is not None
        annotation: Any = field_info.annotation
        default = ... if field_info.default is PydanticUndefined else field_info.default
        is_credential = field_name in credential_fields

        if field_name == "id":
            read_fields[field_name] = (annotation, default)
            continue

        if not is_credential:
            read_fields[field_name] = (annotation, default)

        # Credential fields are write-only: input on create/update, never on read.
        create_fields[field_name] = (annotation, default)
        update_fields[field_name] = (annotation | None, None)

    config = ConfigDict(extra="forbid")
    read_schema = create_model(f"{name}Read", __config__=config, **read_fields)
    create_schema = create_model(f"{name}Create", __config__=config, **create_fields)
    update_schema = create_model(f"{name}Update", __config__=config, **update_fields)
    return read_schema, create_schema, update_schema
