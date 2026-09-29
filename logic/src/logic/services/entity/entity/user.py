"""Child Service for the User Entity."""

from typing import Any, ClassVar

from model.interface import User

from logic.core.protection import hash_value, protect_entity
from logic.services.entity.base_entity import BaseEntity
from logic.services.storage import interface as storage
from logic.services.storage.interface import DatabaseInstance


class UserService(BaseEntity):
    """Entity-bound Actions for User records.

    The password and api_key of a User are stored only as one-way hashes.
    """

    entity = User
    _hashed: ClassVar[tuple[str, ...]] = ("password", "api_key")

    @classmethod
    def _treatments(cls) -> dict[str, Any]:
        """Return the protection applied to each credential Field."""
        return dict.fromkeys(cls._hashed, hash_value)

    @classmethod
    def add(cls, entity: Any, instance: DatabaseInstance | None = None) -> Any:
        """Persist a User whose credentials are stored as hashes.

        Args:
            entity (Any): User instance carrying the plain credentials.
            instance (DatabaseInstance, optional): Instance to use; Database's default when omitted.

        Returns:
            (Any): The created User, carrying the stored hashes.

        Raises:
            TypeError: When the instance is not a User; nothing reaches Storage.
        """
        cls._require(entity)
        return super().add(protect_entity(entity, cls._treatments()), instance)

    @classmethod
    def update(cls, entity: Any, instance: DatabaseInstance | None = None) -> Any:
        """Update a User; a credential left unchanged keeps its stored hash.

        Args:
            entity (Any): User instance carrying the id of the record.
            instance (DatabaseInstance, optional): Instance to use; Database's default when omitted.

        Returns:
            (Any): The updated User, or None when no record has that id.

        Raises:
            TypeError: When the instance is not a User; nothing reaches Storage.
        """
        cls._require(entity)
        stored = storage.storage_get_by_id(cls.entity, entity.id, instance)
        if stored is None:
            return super().update(entity, instance)
        return super().update(
            protect_entity(entity, cls._treatments(), stored), instance
        )
