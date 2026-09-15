"""Verifies serialization and schema generation for every Domain Definition."""

from __future__ import annotations

import json

from model import Account


def test_model_dump_round_trips_every_domain_definition(
    domain_sample: tuple[type, dict[str, object]],
) -> None:
    domain_cls, data = domain_sample
    instance = domain_cls(**data)
    dumped = instance.model_dump()
    reconstructed = domain_cls(**dumped)
    assert reconstructed == instance


def test_model_dump_json_produces_valid_json(
    domain_sample: tuple[type, dict[str, object]],
) -> None:
    domain_cls, data = domain_sample
    instance = domain_cls(**data)
    payload = instance.model_dump_json()
    assert json.loads(payload)["id"] == data["id"]


def test_json_schema_generation_publishes_persistence_metadata() -> None:
    schema = Account.model_json_schema()
    id_schema = schema["properties"]["id"]
    assert id_schema["primary_key"] is True
    assert id_schema["auto_increment"] is True
    group_id_schema = schema["properties"]["group_id"]
    assert group_id_schema["foreign_key"] == "account_group.id"
