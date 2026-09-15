"""Verifies P1T1: the shared Model Foundation.

Two unrelated Domain Definitions realized on the Foundation must both expose
consistent validation, serialization, and metadata-publication behavior while
declaring completely independent Fields and relationships.
"""

from __future__ import annotations

import pytest
from pydantic import Field, ValidationError

from model.foundation import DomainModel, field_meta


class _Alpha(DomainModel):
    __persistent__ = True
    id: int = Field(json_schema_extra=field_meta(primary_key=True, auto_increment=True))
    label: str = Field(json_schema_extra=field_meta(unique=True))


class _Beta(DomainModel):
    __persistent__ = False
    __unique_sets__ = (("owner_id", "code"),)
    id: int = Field(json_schema_extra=field_meta(primary_key=True, auto_increment=True))
    owner_id: int = Field(json_schema_extra=field_meta(foreign_key="alpha.id"))
    code: str = Field(json_schema_extra=field_meta())


def test_unrelated_models_share_validation_behavior() -> None:
    with pytest.raises(ValidationError):
        _Alpha()  # pyright: ignore[reportCallIssue]  # required fields intentionally missing
    with pytest.raises(ValidationError):
        _Beta()  # pyright: ignore[reportCallIssue]  # required fields intentionally missing


def test_unrelated_models_share_serialization_behavior() -> None:
    alpha = _Alpha(id=1, label="a")
    beta = _Beta(id=1, owner_id=1, code="b")
    assert alpha.model_dump() == {"id": 1, "label": "a"}
    assert beta.model_dump() == {"id": 1, "owner_id": 1, "code": "b"}


def test_unrelated_models_have_independent_fields_and_metadata() -> None:
    alpha_fields = set(_Alpha.model_fields)
    beta_fields = set(_Beta.model_fields)
    assert alpha_fields == {"id", "label"}
    assert beta_fields == {"id", "owner_id", "code"}
    assert alpha_fields.isdisjoint(beta_fields - {"id"})

    alpha_meta = _Alpha.persistence_metadata()
    beta_meta = _Beta.persistence_metadata()
    assert alpha_meta["persistent"] is True
    assert beta_meta["persistent"] is False
    assert beta_meta["unique_sets"] == [["owner_id", "code"]]
    assert alpha_meta["unique_sets"] == []
