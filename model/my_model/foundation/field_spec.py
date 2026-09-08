"""What one field of an entity carries, before and after completion.

A definition states only the properties that matter to it. Everything it leaves
unstated is completed from the applicable defaults, so a short declaration and a
fully stated one produce the same resolved field.
"""

from __future__ import annotations

from dataclasses import dataclass, fields as dataclass_fields, replace
from typing import Any

from .credentials import CredentialStorage
from .unset import UNSET, is_stated


class FieldType(str):
    """The logical type of a field, independent of any storage or transport form."""

    INTEGER = "integer"
    STRING = "string"
    BOOLEAN = "boolean"
    DECIMAL = "decimal"
    FLOAT = "float"
    DATETIME = "datetime"


@dataclass(frozen=True, slots=True)
class FieldSpec:
    """One field's logical properties, any of which may be left unstated."""

    type: Any = UNSET
    nullable: Any = UNSET
    unique: Any = UNSET
    primary_key: Any = UNSET
    auto_increment: Any = UNSET
    size: Any = UNSET
    default: Any = UNSET
    credential: Any = UNSET
    credential_storage: Any = UNSET
    purpose: Any = UNSET

    def stated_properties(self) -> dict[str, Any]:
        """The properties this specification actually states."""

        return {
            item.name: getattr(self, item.name)
            for item in dataclass_fields(self)
            if is_stated(getattr(self, item.name))
        }

    def completed_with(self, defaults: dict[str, Any]) -> FieldSpec:
        """This specification with its unstated properties taken from ``defaults``.

        Completion is per property: a stated property is kept as it is, empty
        values included, and a default never replaces one.
        """

        known = {item.name for item in dataclass_fields(self)}
        missing = {
            name: value
            for name, value in defaults.items()
            if name in known and not is_stated(getattr(self, name))
        }
        return replace(self, **missing) if missing else self

    def is_credential(self) -> bool:
        return is_stated(self.credential) and bool(self.credential)

    def storage_treatment(self) -> CredentialStorage | None:
        """The treatment this field requires at rest, or ``None`` if it is not a credential."""

        if not self.is_credential() or not is_stated(self.credential_storage):
            return None
        return CredentialStorage(self.credential_storage)

    def is_required_in_state(self) -> bool:
        """Whether the resulting domain state must carry a value for this field."""

        return is_stated(self.nullable) and not self.nullable
