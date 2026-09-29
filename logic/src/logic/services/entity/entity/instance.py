"""Child Service for the Instance Entity."""

from typing import Any, ClassVar

from model.interface import Account, Instance

from logic.core.protection import (
    encrypt_value,
    protect_entity,
    reveal_value,
    same_value,
)
from logic.services.entity.base_entity import BaseEntity
from logic.services.storage import interface as storage
from logic.services.storage.interface import DatabaseInstance


class InstanceService(BaseEntity):
    """Entity-bound Actions for Instance records.

    The password and api_key of an Instance are stored only in encrypted form, and neither may
    equal the password of an Account that uses the Instance.
    """

    entity = Instance
    _encrypted: ClassVar[tuple[str, ...]] = ("password", "api_key")

    @classmethod
    def _treatments(cls) -> dict[str, Any]:
        """Return the protection applied to each credential Field."""
        return dict.fromkeys(cls._encrypted, encrypt_value)

    @classmethod
    def add(cls, entity: Any, instance: DatabaseInstance | None = None) -> Any:
        """Persist an Instance whose credentials are stored encrypted.

        Args:
            entity (Any): Instance record carrying the plain credentials.
            instance (DatabaseInstance, optional): Instance to use; Database's default when omitted.

        Returns:
            (Any): The created Instance record, carrying the encrypted credentials.

        Raises:
            TypeError: When the instance is not an Instance record; nothing reaches Storage.
            ValueError: When a required runtime value is missing or invalid.
        """
        cls._require(entity)
        return super().add(protect_entity(entity, cls._treatments()), instance)

    @classmethod
    def update(cls, entity: Any, instance: DatabaseInstance | None = None) -> Any:
        """Update an Instance record; a credential left unchanged keeps its stored form.

        Args:
            entity (Any): Instance record carrying the id of the record.
            instance (DatabaseInstance, optional): Instance to use; Database's default when omitted.

        Returns:
            (Any): The updated Instance record, or None when no record has that id.

        Raises:
            TypeError: When the instance is not an Instance record; nothing reaches Storage.
            ValueError: When a changed credential equals the password of an Account using the
                Instance, or a required runtime value is missing or invalid.
        """
        cls._require(entity)
        stored = storage.storage_get_by_id(cls.entity, entity.id, instance)
        if stored is None:
            return super().update(entity, instance)
        cls._refuse_shared_credential(entity, stored, instance)
        return super().update(
            protect_entity(entity, cls._treatments(), stored), instance
        )

    @classmethod
    def _refuse_shared_credential(
        cls, entity: Any, stored: Any, instance: DatabaseInstance | None
    ) -> None:
        """Refuse a changed credential equal to the password of an Account using the Instance."""
        changed = [
            getattr(entity, field)
            for field in cls._encrypted
            if getattr(entity, field) is not None
            and getattr(entity, field) != getattr(stored, field)
        ]
        if not changed:
            return
        accounts = storage.storage_list(Account, None, None, None, None, instance)
        for account in accounts:
            if account.instance_id != entity.id:
                continue
            password = reveal_value(account.password)
            if any(same_value(password, value) for value in changed):
                raise ValueError(
                    "An Instance credential must not duplicate the password "
                    "of an Account that uses the Instance"
                )
