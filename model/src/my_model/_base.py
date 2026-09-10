from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, Field

from ._shared import Relationship


class DomainModel(BaseModel):
    id: int | None = Field(default=None)

    credential_fields: ClassVar[frozenset[str]] = frozenset()
    credential_storage: ClassVar[dict[str, str]] = {}
    unique_fields: ClassVar[frozenset[str]] = frozenset()
    unique_together: ClassVar[list[tuple[str, ...]]] = []
    relationships: ClassVar[dict[str, Relationship]] = {}
    domain_rules: ClassVar[list[str]] = []
