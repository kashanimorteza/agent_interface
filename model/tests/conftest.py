"""Shared verification helpers for every Domain Definition test module."""

from __future__ import annotations

from model.foundation import DomainModel


def assert_serializes_and_generates_schema(instance: DomainModel) -> None:
    """Prove the foundation's serialization and schema-generation mechanisms
    work correctly for a concrete, valid Domain Definition instance."""
    cls = type(instance)

    dumped = instance.model_dump()
    for field in cls.model_fields:
        assert field in dumped

    round_tripped = cls.model_validate_json(instance.model_dump_json())
    assert round_tripped == instance

    schema = cls.model_json_schema()
    assert schema["title"] == cls.__name__
    for field in cls.model_fields:
        assert field in schema["properties"]


def assert_rejects_unknown_field(cls: type[DomainModel], valid_data: dict) -> None:
    """Prove declarative validation rejects data outside the declared Fields."""
    import pytest
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        cls.model_validate({**valid_data, "not_a_declared_field": "x"})


def assert_requires_field(
    cls: type[DomainModel], valid_data: dict, required_field: str
) -> None:
    """Prove a non-nullable, non-defaulted Field is required."""
    import pytest
    from pydantic import ValidationError

    incomplete = dict(valid_data)
    incomplete.pop(required_field)
    with pytest.raises(ValidationError):
        cls.model_validate(incomplete)
