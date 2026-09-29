"""Child Service for the Account Entity."""

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


class AccountService(BaseEntity):
    """Entity-bound Actions for Account records.

    The password of an Account is stored only in encrypted form and never equals the password
    or api_key of the Instance the Account uses.
    """

    entity = Account
    _encrypted: ClassVar[tuple[str, ...]] = ("password",)

    @classmethod
    def _treatments(cls) -> dict[str, Any]:
        """Return the protection applied to each credential Field."""
        return dict.fromkeys(cls._encrypted, encrypt_value)

    @classmethod
    def add(cls, entity: Any, instance: DatabaseInstance | None = None) -> Any:
        """Persist an Account whose password is stored encrypted.

        Args:
            entity (Any): Account instance carrying the plain password.
            instance (DatabaseInstance, optional): Instance to use; Database's default when omitted.

        Returns:
            (Any): The created Account, carrying the encrypted password.

        Raises:
            TypeError: When the instance is not an Account; nothing reaches Storage.
            ValueError: When the password duplicates a credential of the Account's Instance, or
                a required runtime value is missing or invalid.
        """
        cls._require(entity)
        cls._refuse_shared_credential(entity.password, entity.instance_id, instance)
        return super().add(protect_entity(entity, cls._treatments()), instance)

    @classmethod
    def update(cls, entity: Any, instance: DatabaseInstance | None = None) -> Any:
        """Update an Account; an unchanged password keeps its stored form.

        Args:
            entity (Any): Account instance carrying the id of the record.
            instance (DatabaseInstance, optional): Instance to use; Database's default when omitted.

        Returns:
            (Any): The updated Account, or None when no record has that id.

        Raises:
            TypeError: When the instance is not an Account; nothing reaches Storage.
            ValueError: When the password duplicates a credential of the Account's Instance, or
                a required runtime value is missing or invalid.
        """
        cls._require(entity)
        stored = storage.storage_get_by_id(cls.entity, entity.id, instance)
        if stored is None:
            return super().update(entity, instance)
        plain = (
            reveal_value(stored.password)
            if entity.password == stored.password
            else entity.password
        )
        cls._refuse_shared_credential(plain, entity.instance_id, instance)
        return super().update(
            protect_entity(entity, cls._treatments(), stored), instance
        )

    @classmethod
    def _refuse_shared_credential(
        cls, plain: str, instance_id: int, instance: DatabaseInstance | None
    ) -> None:
        """Refuse a password equal to the password or api_key of the Account's Instance."""
        used = storage.storage_get_by_id(Instance, instance_id, instance)
        if used is None:
            return
        for credential in (used.password, used.api_key):
            if credential is not None and same_value(plain, reveal_value(credential)):
                raise ValueError(
                    "An Account password must not duplicate the password "
                    "or api_key of its Instance"
                )
