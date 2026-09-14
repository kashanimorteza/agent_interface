"""Shared verification helpers (Model Preferences: implementation.verification.checks).

Each helper proves one category of behaviour every Domain Definition must exhibit, so a
per-model test only supplies that Domain Definition's own valid data and field lists — the
generic proof (public interface, validation behaviour, serialization/schema) is defined once.
"""

from __future__ import annotations

import copy
from typing import Any

import pydantic
import pytest


def assert_public_interface(
    model_module: Any, name: str, cls: type[pydantic.BaseModel]
) -> None:
    """Prove the Domain Definition has one unambiguous public identity (Model Principle 5)."""
    assert getattr(model_module, name) is cls
    assert name in model_module.__all__


def assert_valid_construction[ModelT: pydantic.BaseModel](
    cls: type[ModelT], valid_data: dict[str, Any]
) -> ModelT:
    """Prove valid Target-consistent data is accepted."""
    instance = cls(**valid_data)
    for key, value in valid_data.items():
        assert getattr(instance, key) == value
    return instance


def assert_rejects_unknown_field(
    cls: type[pydantic.BaseModel], valid_data: dict[str, Any]
) -> None:
    """Prove strict unknown-Field rejection (Foundation-enforced convention)."""
    with pytest.raises(pydantic.ValidationError):
        cls(**valid_data, unexpected_field="anything")


def assert_rejects_missing_required(
    cls: type[pydantic.BaseModel],
    valid_data: dict[str, Any],
    required_fields: list[str],
) -> None:
    """Prove every declared required Field is individually enforced — one passing example does
    not prove a compound requirement, so every required Field is checked on its own."""
    for field_name in required_fields:
        incomplete = copy.deepcopy(valid_data)
        del incomplete[field_name]
        with pytest.raises(pydantic.ValidationError):
            cls(**incomplete)


def assert_rejects_null_for_non_nullable(
    cls: type[pydantic.BaseModel],
    valid_data: dict[str, Any],
    non_nullable_fields: list[str],
) -> None:
    """Prove every declared non-nullable Field individually rejects `null` (Model Principle 6)."""
    for field_name in non_nullable_fields:
        invalid = copy.deepcopy(valid_data)
        invalid[field_name] = None
        with pytest.raises(pydantic.ValidationError):
            cls(**invalid)


def assert_rejects_wrong_type(
    cls: type[pydantic.BaseModel], valid_data: dict[str, Any], field_name: str
) -> None:
    """Prove a Field rejects data of the wrong type rather than silently coercing it."""
    invalid = copy.deepcopy(valid_data)
    invalid[field_name] = object()
    with pytest.raises(pydantic.ValidationError):
        cls(**invalid)


def assert_serialization_roundtrip(instance: pydantic.BaseModel) -> None:
    """Prove schema and serialization round-trip preserve every declared Field."""
    cls = type(instance)

    dumped = instance.model_dump()
    rebuilt = cls(**dumped)
    assert rebuilt == instance

    dumped_json = instance.model_dump_json()
    rebuilt_from_json = cls.model_validate_json(dumped_json)
    assert rebuilt_from_json == instance

    schema = cls.model_json_schema()
    for field_name in type(instance).model_fields:
        assert field_name in schema["properties"]
