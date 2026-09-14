import base64
import hashlib
import os
import secrets
from datetime import UTC
from typing import Any

from cryptography.fernet import Fernet
from model.foundation import CredentialStorage, ModelBase
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.types import TypeDecorator

_PBKDF2_ITERATIONS = 600_000


class StorageBase(DeclarativeBase):
    pass


class UTCDateTime(TypeDecorator[Any]):
    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value: Any, dialect: Any) -> Any:
        if value is None:
            return None
        if value.tzinfo is None:
            raise ValueError("UTCDateTime requires a timezone-aware datetime")
        return value.astimezone(UTC).replace(tzinfo=None)

    def process_result_value(self, value: Any, dialect: Any) -> Any:
        if value is None:
            return None
        return value.replace(tzinfo=UTC)


def hash_credential(value: str) -> str:
    salt = secrets.token_bytes(16)
    derived = hashlib.pbkdf2_hmac(
        "sha256", value.encode("utf-8"), salt, _PBKDF2_ITERATIONS
    )
    return f"{base64.b64encode(salt).decode()}${base64.b64encode(derived).decode()}"


def verify_hashed_credential(candidate: str, stored: str) -> bool:
    salt_b64, derived_b64 = stored.split("$", 1)
    salt = base64.b64decode(salt_b64)
    expected = base64.b64decode(derived_b64)
    derived = hashlib.pbkdf2_hmac(
        "sha256", candidate.encode("utf-8"), salt, _PBKDF2_ITERATIONS
    )
    return secrets.compare_digest(derived, expected)


def _encryption_key() -> bytes:
    raw = os.environ.get("DATABASE_ENCRYPTION_KEY")
    if not raw:
        raise RuntimeError(
            "DATABASE_ENCRYPTION_KEY environment variable is required to protect or reveal "
            "a reversible (encrypted) credential field."
        )
    return raw.encode("utf-8")


def encrypt_credential(value: str) -> str:
    return Fernet(_encryption_key()).encrypt(value.encode("utf-8")).decode("utf-8")


def decrypt_credential(stored: str) -> str:
    return Fernet(_encryption_key()).decrypt(stored.encode("utf-8")).decode("utf-8")


def protect_credential(value: str, mode: CredentialStorage) -> str:
    if mode is CredentialStorage.HASH:
        return hash_credential(value)
    return encrypt_credential(value)


def reveal_credential(stored: str, mode: CredentialStorage) -> str | None:
    if mode is CredentialStorage.HASH:
        return None
    return decrypt_credential(stored)


def verify_credential(candidate: str, stored: str, mode: CredentialStorage) -> bool:
    if mode is CredentialStorage.HASH:
        return verify_hashed_credential(candidate, stored)
    return decrypt_credential(stored) == candidate


def credential_fields(model_type: type[ModelBase]) -> dict[str, CredentialStorage]:
    result: dict[str, CredentialStorage] = {}
    for name, field in model_type.model_fields.items():
        extra = field.json_schema_extra
        if isinstance(extra, dict) and "credential_storage" in extra:
            result[name] = CredentialStorage(extra["credential_storage"])
    return result
