"""Shared base class and package-wide conventions for every my_model domain entity."""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict


class GenerateSecurely:
    """Sentinel marking an initial-data value that must be generated securely at
    persistence time rather than stored as a literal credential in source or Config.
    """

    _instance: ClassVar[GenerateSecurely | None] = None

    def __new__(cls) -> GenerateSecurely:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:  # pragma: no cover - debugging aid only
        return "GENERATE_SECURELY"


GENERATE_SECURELY = GenerateSecurely()


class BaseModel(PydanticBaseModel):
    """Shared base for every my_model domain entity.

    Provides the package-wide validation configuration and the declared-credential
    and declared-initial-data conventions every entity uses, without deciding how
    a credential is stored, hashed, or transported, and without performing any
    insertion of its own declared initial records.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
    )

    #: Names of fields that carry credential or otherwise sensitive domain meaning.
    #: Storage, hashing, encryption, and transport masking belong to other components.
    credential_fields: ClassVar[frozenset[str]] = frozenset()

    #: Domain records that must logically exist when the project begins. Values may
    #: be a :data:`GENERATE_SECURELY` sentinel for a credential that must be generated
    #: rather than a literal value. Insertion belongs to Database, never to Model.
    initial_data: ClassVar[tuple[dict[str, Any], ...]] = ()
