"""Verifies the Model Foundation contributes no Field or relationship of its own."""

from typing import Annotated

import pytest
from pydantic import ValidationError

from model.foundation import (
    DomainModel,
    FieldMeta,
    ForeignKey,
    PersistenceMeta,
    persistence_contract,
)


def test_domain_model_declares_no_fields() -> None:
    assert DomainModel.model_fields == {}


def test_domain_model_forbids_unknown_fields_and_validates_on_assignment() -> None:
    class Minimal(DomainModel):
        value: Annotated[int, FieldMeta(nullable=False)]

    instance = Minimal(value=1)
    assert instance.value == 1

    with pytest.raises(ValidationError):
        Minimal(value=1, unexpected="nope")  # type: ignore[call-arg]

    with pytest.raises(ValidationError):
        instance.value = "not-an-int"  # type: ignore[assignment]


def test_persistence_contract_publishes_field_and_model_metadata() -> None:
    class Minimal(DomainModel):
        id: Annotated[int | None, FieldMeta(primary_key=True, auto_increment=True)] = None
        owner_id: Annotated[int, FieldMeta(nullable=False, foreign_key=ForeignKey("User", "id"))]
        name: Annotated[str, FieldMeta(nullable=False, unique=True)]

        class Meta(PersistenceMeta):
            persistent = True
            unique_sets = (("owner_id", "name"),)

    contract = persistence_contract(Minimal)
    assert contract.persistent is True
    assert contract.unique_sets == (("owner_id", "name"),)

    by_name = {f.name: f.meta for f in contract.fields}
    assert by_name["id"].primary_key is True
    assert by_name["id"].auto_increment is True
    assert by_name["owner_id"].foreign_key == ForeignKey("User", "id")
    assert by_name["name"].unique is True


def test_persistence_contract_defaults_missing_field_meta_from_required_state() -> None:
    class Minimal(DomainModel):
        required_value: int
        optional_value: int | None = None

    contract = persistence_contract(Minimal)
    by_name = {f.name: f.meta for f in contract.fields}
    assert by_name["required_value"].nullable is False
    assert by_name["optional_value"].nullable is True
