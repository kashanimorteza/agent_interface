from typing import Any

from model.foundation import ModelBase
from pydantic import SecretStr

from .foundation import (
    StorageBase,
    credential_fields,
    protect_credential,
    reveal_credential,
)


def to_orm_kwargs(instance: ModelBase) -> dict[str, Any]:
    modes = credential_fields(type(instance))
    data = instance.model_dump(exclude={"id"})
    for name, mode in modes.items():
        raw = getattr(instance, name)
        if raw is None:
            data[name] = None
        else:
            plain = raw.get_secret_value() if isinstance(raw, SecretStr) else raw
            data[name] = protect_credential(plain, mode)
    return data


def from_orm_row(model_type: type[ModelBase], row: StorageBase) -> ModelBase:
    modes = credential_fields(model_type)
    data: dict[str, Any] = {}
    for name in model_type.model_fields:
        value = getattr(row, name)
        if name in modes and value is not None:
            revealed = reveal_credential(value, modes[name])
            data[name] = revealed if revealed is not None else value
        else:
            data[name] = value
    return model_type.model_validate(data)
