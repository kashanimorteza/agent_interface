"""Verifies the Model Foundation provides shared mechanisms without owning any Field."""

from __future__ import annotations

from model import ModelBase
from model.foundation import persistence_field


def test_foundation_declares_no_domain_field() -> None:
    assert ModelBase.model_fields == {}


def test_every_domain_definition_publishes_a_persistence_contract(
    domain_sample: tuple[type, dict[str, object]],
) -> None:
    domain_cls, _data = domain_sample
    contract = domain_cls.persistence_contract()
    assert contract["persistent"] is True
    assert "id" in contract["fields"]
    assert contract["fields"]["id"]["primary_key"] is True
    assert contract["fields"]["id"]["auto_increment"] is True


def test_foreign_key_fields_publish_cardinality() -> None:
    from model import Instance

    contract = Instance.persistence_contract()
    assert contract["fields"]["user_id"]["foreign_key"] == "user.id"
    assert contract["fields"]["user_id"]["cardinality"] == "one"


def test_credential_fields_publish_declared_treatment() -> None:
    from model import Instance, User

    user_contract = User.persistence_contract()
    assert user_contract["fields"]["password"]["credential"] == "hash"
    assert user_contract["fields"]["api_key"]["credential"] == "hash"

    instance_contract = Instance.persistence_contract()
    assert instance_contract["fields"]["password"]["credential"] == "encrypted"
    assert instance_contract["fields"]["api_key"]["credential"] == "encrypted"


def test_composite_unique_sets_are_published() -> None:
    from model import Account

    contract = Account.persistence_contract()
    assert contract["unique_sets"] == [["group_id", "broker_id", "instance_id"]]


def test_persistence_field_never_adds_a_field_to_the_foundation_itself() -> None:
    # Calling the Foundation's own field-declaration mechanism does not
    # register a Field on ModelBase; it only produces a FieldInfo for the
    # concrete Domain Definition that assigns it to one of its own attributes.
    persistence_field(default=1)
    assert ModelBase.model_fields == {}
