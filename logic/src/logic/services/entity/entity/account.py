"""The Account Service."""

import hmac
from collections.abc import Mapping
from typing import Any, ClassVar

from model.interface import Account, Instance

from logic.core.credentials import WITHHELD, Treatment
from logic.core.outcome import Outcome, OutcomeKind
from logic.services.entity.base import EntityServiceBase

_INSTANCE_CREDENTIALS = ("password", "api_key")


class AccountService(EntityServiceBase[Account]):
    """Entity-bound Actions for Account records; an Account never reuses a credential of its Instance."""

    entity = Account
    credentials: ClassVar[Mapping[str, Treatment]] = {"password": Treatment.ENCRYPTED}

    def add(self, entity: Account) -> Outcome[Account]:
        """Persist a new Account unless its credential duplicates one of its Instance.

        Args:
            entity (Account): Complete Account instance.

        Returns:
            (Outcome): The shared Add outcome, or an invalid failure for a duplicated credential.
        """
        return self._duplicated(entity) or super().add(entity)

    def update(self, entity: Account) -> Outcome[Account]:
        """Replace an Account's mutable Fields unless its credential duplicates one of its Instance.

        Args:
            entity (Account): Complete Account instance holding the id of the record.

        Returns:
            (Outcome): The shared Update outcome, or an invalid failure for a duplicated credential.
        """
        return self._duplicated(entity) or super().update(entity)

    def _duplicated(self, entity: Account) -> Outcome[Any] | None:
        if not isinstance(entity, Account):
            return None
        candidate: str | None = entity.password
        if candidate == WITHHELD:
            record_id = entity.id
            if record_id is None:
                return None
            stored = self._dependency.call(
                lambda: self._database.get_by_id(Account, record_id), repeatable=True
            )
            if not stored.succeeded or stored.value is None:
                return stored if not stored.succeeded else None
            candidate = self._original(stored.value.password)
        if candidate is None:
            return None
        instance = self._dependency.call(
            lambda: self._database.get_by_id(Instance, entity.instance_id),
            repeatable=True,
        )
        if not instance.succeeded or instance.value is None:
            return instance if not instance.succeeded else None
        originals = (
            self._original(getattr(instance.value, name))
            for name in _INSTANCE_CREDENTIALS
        )
        if any(
            value is not None
            and hmac.compare_digest(value.encode(), candidate.encode())
            for value in originals
        ):
            return Outcome.failure(
                OutcomeKind.INVALID,
                "an Account cannot reuse a credential of its Instance",
            )
        return None

    def _original(self, stored: str | None) -> str | None:
        if stored is None:
            return None
        return self._protector.recover(stored) or stored
