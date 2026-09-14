"""The Model Foundation shared by every concrete Domain Definition in this package."""

from __future__ import annotations

import datetime
from typing import Annotated, ClassVar

from pydantic import AfterValidator, BaseModel, ConfigDict


class ModelBase(BaseModel):
    """Shared configuration and behavior every Domain Definition inherits.

    Every concrete Domain Definition receives this same configuration rather than
    declaring it independently: unknown fields are rejected, assignment is
    re-validated, and string fields are stripped of incidental whitespace.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
    )

    UNIQUE_CONSTRAINTS: ClassVar[tuple[tuple[str, ...], ...]] = ()


def _require_timezone_aware(value: datetime.datetime) -> datetime.datetime:
    if value.tzinfo is None:
        raise ValueError("datetime value must be timezone-aware")
    return value


TimezoneAwareDatetime = Annotated[datetime.datetime, AfterValidator(_require_timezone_aware)]
"""A datetime value that Model rejects unless it carries timezone information."""

UniqueConstraints = tuple[tuple[str, ...], ...]
"""The declarative shape of a Domain Definition's declared uniqueness constraints."""
