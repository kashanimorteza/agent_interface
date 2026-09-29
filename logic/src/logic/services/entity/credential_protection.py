"""Credential Fields stored hashed or encrypted at rest, as the Target requires."""

from typing import Any, ClassVar, Literal

from logic.core import config, credentials
from logic.services.entity.base_entity import BaseEntity
from logic.services.storage import interface as storage
from logic.services.storage.interface import DatabaseInstance

PROTECTION_KEY = "credential_protection_key"


class ProtectedCredentials(BaseEntity):
    """Base Entity whose credential Fields reach Storage only hashed or encrypted.

    A value equal to the one already stored is kept as it is, so updating another Field of a
    record never treats a stored credential a second time.

    Attributes:
        credential_fields: Names of the credential Fields.
        treatment: "hash" stores one-way hashes; "encrypt" stores tokens Logic can decrypt.
    """

    credential_fields: ClassVar[tuple[str, ...]]
    treatment: ClassVar[Literal["hash", "encrypt"]]

    def _prepare(self, entity: Any) -> tuple[list[str], str | None]:
        self._check(entity)
        fields = [f for f in self.credential_fields if getattr(entity, f) is not None]
        key = (
            config.require(PROTECTION_KEY)
            if fields and self.treatment == "encrypt"
            else None
        )
        return fields, key

    def _protected(
        self, entity: Any, fields: list[str], key: str | None, stored: Any
    ) -> Any:
        changes = {}
        for field in fields:
            value = getattr(entity, field)
            if stored is not None and value == getattr(stored, field):
                continue
            changes[field] = (
                credentials.hash_secret(value)
                if key is None
                else credentials.encrypt_secret(value, key)
            )
        if not changes:
            return entity
        return type(entity).from_json({**entity.to_json(), **changes})

    def add(self, entity: Any, instance: DatabaseInstance | None = None) -> Any:
        """Persist a complete Entity instance with its credentials protected."""
        fields, key = self._prepare(entity)
        return super().add(self._protected(entity, fields, key, None), instance)

    def update(self, entity: Any, instance: DatabaseInstance | None = None) -> Any:
        """Update a record, protecting each credential that differs from the stored one."""
        fields, key = self._prepare(entity)
        stored = (
            storage.storage_get_by_id(self.entity, entity.id, instance)
            if fields and entity.id is not None
            else None
        )
        return super().update(self._protected(entity, fields, key, stored), instance)
