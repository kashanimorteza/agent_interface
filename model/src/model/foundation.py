"""Model Foundation: shared configuration and behavior for every Domain Definition."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any, ClassVar

from pydantic import AfterValidator, BaseModel, ConfigDict, Field

type UniqueConstraints = tuple[tuple[str, ...], ...]


class ModelBase(BaseModel):
    """Shared base for every concrete Domain Definition in this package."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        validate_default=True,
    )

    # Uniqueness is domain meaning stated by the Target, so Model declares it.
    # Evaluating it needs records other than this one, so Model never enforces it.
    unique_constraints: ClassVar[UniqueConstraints] = ()


def identity_field(**overrides: Any) -> Any:
    """A Field for an auto-generated primary identity, supplied by an external generation mechanism."""

    defaults: dict[str, Any] = {
        "description": "Auto-generated primary identity.",
        "json_schema_extra": {"identity": True, "generated": True},
    }
    defaults.update(overrides)
    return Field(**defaults)


def credential_field(**overrides: Any) -> Any:
    """A Field carrying credential meaning; storage mechanism is owned outside Model."""

    defaults: dict[str, Any] = {"json_schema_extra": {"credential": True}}
    defaults.update(overrides)
    return Field(**defaults)


def _require_timezone_aware(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise ValueError("Absolute instants must be timezone-aware.")
    return value


TimezoneAwareDatetime = Annotated[datetime, AfterValidator(_require_timezone_aware)]
