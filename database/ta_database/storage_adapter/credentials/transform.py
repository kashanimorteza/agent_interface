"""Apply the at-rest transformation recorded on each credential column."""

from __future__ import annotations

from typing import Any, Mapping

from ta_database.storage_adapter.credentials.encryption import encrypt_credential
from ta_database.storage_adapter.credentials.hashing import hash_credential

INFO_KEY = "credential_storage"


def credential_modes(mapped_class: type) -> dict[str, str]:
    return {c.name: c.info[INFO_KEY] for c in mapped_class.__table__.columns if INFO_KEY in c.info}


def credential_columns(mapped_class: type) -> set[str]:
    return set(credential_modes(mapped_class))


def transform_value(mode: str, value: Any) -> Any:
    if value is None:
        return None
    if mode == "hash":
        return hash_credential(str(value))
    if mode == "encrypted":
        return encrypt_credential(str(value))
    if mode == "plaintext":
        return value
    raise ValueError(f"unsupported credential storage mode: {mode}")


def apply_write_transforms(mapped_class: type, data: Mapping[str, Any]) -> dict[str, Any]:
    """Return a new dict with every credential key transformed by its column's mode."""
    modes = credential_modes(mapped_class)
    return {k: (transform_value(modes[k], v) if k in modes else v) for k, v in data.items()}
