"""Model Foundation: shared configuration and behaviour for every Domain Definition (Model Principle 4).

Every concrete Domain Definition in this package is built through `ModelFoundation` so that
common Field defaults, strict unknown-Field rejection, deterministic side-effect-free validation,
exact-decimal numeric handling, and timezone-aware UTC time handling are defined exactly once
instead of being redeclared by each Domain Definition (Model Principle 4, Model Preferences
`implementation`).
"""

from __future__ import annotations

import datetime
import decimal
import itertools
from typing import Annotated, Any, ClassVar

import pydantic

DEFAULT_MODEL_OPERATIONS: frozenset[str] = frozenset(
    {"create", "get_by_id", "list", "search", "update", "enable", "disable", "delete"}
)
"""The shared Model Operation vocabulary (Development Principle 5). Every Domain Definition in
this phase applies the complete default set; a later phase may narrow or extend it per Domain
Definition if the Target ever states a Model-specific lifecycle difference."""


def _reject_float(value: Any) -> Any:
    """Reject float input for exact-decimal Fields.

    Coercing a float to Decimal can silently hide invalid domain data (binary floating-point
    values do not exactly represent most decimal fractions), so float input is rejected rather
    than coerced (Model Preferences: implementation.validation.strictness).
    """
    if isinstance(value, float):
        # ValueError, not TypeError: pydantic-core only converts ValueError/AssertionError raised
        # by a BeforeValidator into a ValidationError; a TypeError propagates uncaught instead.
        raise ValueError(  # noqa: TRY004
            "exact-decimal fields do not accept float input; use an int, str, or Decimal"
        )
    return value


def _require_timezone_aware_utc(value: Any) -> Any:
    """Require an absolute-instant Field to be timezone-aware, normalized to UTC.

    (Model Preferences: implementation.time — absolute_instants "timezone-aware",
    canonical_timezone "UTC".)
    """
    if isinstance(value, datetime.datetime):
        if value.tzinfo is None:
            raise ValueError(
                "absolute-instant fields require a timezone-aware datetime"
            )
        return value.astimezone(datetime.UTC)
    return value


ExactDecimal = Annotated[decimal.Decimal, pydantic.BeforeValidator(_reject_float)]
"""Reusable exact-decimal Field type for Target Fields explicitly typed `decimal`
(Model Preferences: implementation.numeric_precision.exact_values)."""

UTCDateTime = Annotated[
    datetime.datetime, pydantic.BeforeValidator(_require_timezone_aware_utc)
]
"""Reusable timezone-aware, UTC-normalized Field type for Target Fields explicitly typed
`datetime` (Model Preferences: implementation.time)."""


class ModelFoundation(pydantic.BaseModel):
    """The technology-independent common foundation every concrete Domain Definition receives
    its shared configuration and behaviour through (Model Principle 4)."""

    model_config = pydantic.ConfigDict(
        extra="forbid",  # Model Preferences: implementation.unknown_fields = "reject"
        validate_assignment=True,
        validate_default=True,  # a declared default must satisfy the same Field convention as any other value
    )

    CREDENTIAL_STORAGE: ClassVar[dict[str, str]] = {}
    """Declared storage-at-rest meaning of this Domain Definition's credential Fields, keyed by
    Field name (e.g. {"password": "hash"}); empty when the Domain Definition has no credential
    Fields. Model records this meaning as stated by the Target (Model Principle 2); it never
    implements hashing or encryption itself, which remains a persistence concern outside Model's
    boundary (Model Principle 9)."""

    MODEL_OPERATIONS: ClassVar[frozenset[str]] = DEFAULT_MODEL_OPERATIONS
    """The Model Operations applicable to this Domain Definition's lifecycle (Development
    Principle 5)."""

    @classmethod
    def credential_storage(cls) -> dict[str, str]:
        """Report the declared storage-at-rest meaning of this Domain Definition's credential
        Fields, without implementing the storage mechanism itself."""
        return dict(cls.CREDENTIAL_STORAGE)

    @classmethod
    def model_operations(cls) -> frozenset[str]:
        """Report the Model Operations applicable to this Domain Definition."""
        return cls.MODEL_OPERATIONS


_id_sequence = itertools.count(1)
"""A process-local, Model-owned placeholder identity sequence, used only when a Domain
Definition is constructed without an explicit `id` (Model Principle 6: `generated: true` means
the value is supplied automatically on omission). This is not a persistence-layer auto-increment
and gives no uniqueness or ordering guarantee beyond this process — Model does not select or
depend on the real storage generation mechanism (Model Principle 9); Database (P2) assigns and
owns the definitive persisted identity. An explicit `id` (e.g. one already assigned by
persistence and passed back in for reconstruction, as serialization round-tripping requires)
overrides this placeholder."""


def _generate_id() -> int:
    return next(_id_sequence)


def id_field() -> Any:
    """The common generated identity Field (Model Preferences:
    field_defaults.common_fields.id).

    Declared `generated: true` and `nullable: false` (Model Principle 6): omitting `id` at
    construction resolves it through Model's own placeholder generator (`_generate_id`) rather
    than to `null`, so the identity is generated automatically rather than required from the
    caller. Model does not select the real persistence-layer generation mechanism (Model
    Principle 9) — the placeholder value has no significance beyond this process — but an
    explicit `id` may still be supplied (e.g. by Database reconstructing a previously persisted
    Domain Definition) and is accepted like any other Field value; only an explicit `null` is
    rejected, per `nullable: false`.
    """
    return pydantic.Field(
        default_factory=_generate_id,
        description=(
            "The generated identity of this Domain Definition, supplied automatically when "
            "omitted; Model does not select the persistence-layer generation mechanism, and "
            "an explicit value (e.g. for reconstruction) is still accepted."
        ),
    )


def is_active_field(purpose: str) -> Any:
    """The common `is_active` Field (Model Preferences: field_defaults.common_fields.is_active)."""
    return pydantic.Field(default=True, description=purpose)


def description_field(purpose: str) -> Any:
    """The common nullable `description` Field (Model Preferences:
    field_defaults.common_fields.description)."""
    return pydantic.Field(default=None, description=purpose)
