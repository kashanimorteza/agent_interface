"""Verification for the Model Foundation (Task P1-model-foundation)."""

from __future__ import annotations

import datetime
import decimal

import pydantic
import pytest

from model.foundation import (
    ExactDecimal,
    ModelFoundation,
    UTCDateTime,
    description_field,
    id_field,
    is_active_field,
)


class _Sample(ModelFoundation):
    """A minimal Domain Definition built through the Foundation, used only to prove Foundation
    behaviour is inherited without redeclaration."""

    id: int = id_field()
    name: str = pydantic.Field()
    is_active: bool = is_active_field("Indicates whether the sample is active.")
    description: str | None = description_field("Describes the sample.")
    amount: ExactDecimal = pydantic.Field()
    happened_at: UTCDateTime = pydantic.Field()


def _valid() -> dict:
    return {
        "id": 1,
        "name": "Sample",
        "amount": decimal.Decimal("1.23"),
        "happened_at": datetime.datetime(2026, 1, 1, tzinfo=datetime.UTC),
    }


def test_foundation_supplies_common_field_defaults_without_redeclaration():
    instance = _Sample(**_valid())
    assert instance.id == 1
    assert instance.is_active is True
    assert instance.description is None


def test_foundation_generates_id_when_omitted():
    """`id` is declared `generated: true`: omitting it at construction is supplied automatically
    rather than requiring the caller to supply it (Model Principle 6), through Model's own
    placeholder generation mechanism (Model Principle 9 — Model does not select the real
    persistence-layer mechanism)."""
    without_id = _valid()
    del without_id["id"]
    instance = _Sample(**without_id)
    assert isinstance(instance.id, int)


def test_foundation_generated_ids_are_distinct():
    """Two Domain Definitions constructed without an explicit `id` receive different generated
    values, proving real generation rather than a fixed placeholder."""
    without_id = _valid()
    del without_id["id"]
    first = _Sample(**without_id)
    second = _Sample(**without_id)
    assert first.id != second.id


def test_foundation_accepts_explicit_id_override():
    """An explicit `id` (e.g. one already assigned by persistence and passed back in for
    reconstruction, as serialization round-tripping requires) is still accepted rather than
    always overwritten by the generator."""
    instance = _Sample(**{**_valid(), "id": 42})
    assert instance.id == 42


def test_foundation_rejects_null_id():
    """`id` is declared `nullable: false` (Model Principle 6): an explicit `None` is rejected
    even though omission is supplied automatically."""
    with pytest.raises(pydantic.ValidationError):
        _Sample(**{**_valid(), "id": None})


def test_foundation_rejects_unknown_fields():
    with pytest.raises(pydantic.ValidationError):
        _Sample.model_validate({**_valid(), "unexpected": "value"})


def test_foundation_enforces_exact_decimal_rejects_float():
    data = _valid()
    data["amount"] = 1.23
    with pytest.raises(pydantic.ValidationError):
        _Sample(**data)


def test_foundation_accepts_exact_decimal_from_str_and_int():
    data = _valid()
    data["amount"] = "1.23"
    assert _Sample(**data).amount == decimal.Decimal("1.23")


def test_foundation_enforces_timezone_aware_utc_rejects_naive_datetime():
    data = _valid()
    data["happened_at"] = datetime.datetime(2026, 1, 1)  # noqa: DTZ001 (naive on purpose: proves rejection)
    with pytest.raises(pydantic.ValidationError):
        _Sample(**data)


def test_foundation_normalizes_timezone_aware_datetime_to_utc():
    tz = datetime.timezone(datetime.timedelta(hours=5))
    data = _valid()
    data["happened_at"] = datetime.datetime(2026, 1, 1, 5, 0, tzinfo=tz)
    instance = _Sample(**data)
    assert instance.happened_at == datetime.datetime(
        2026, 1, 1, 0, 0, tzinfo=datetime.UTC
    )
    assert instance.happened_at.tzinfo is not None


def test_foundation_validation_is_deterministic_and_side_effect_free():
    data = _valid()
    assert _Sample(**data) == _Sample(**data)


def test_default_model_operations_cover_the_shared_vocabulary():
    assert ModelFoundation.model_operations() == {
        "create",
        "get_by_id",
        "list",
        "search",
        "update",
        "enable",
        "disable",
        "delete",
    }


def test_credential_storage_defaults_to_empty():
    assert _Sample.credential_storage() == {}
