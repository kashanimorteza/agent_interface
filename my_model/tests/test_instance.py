from __future__ import annotations

import pytest
from pydantic import ValidationError

from my_model._initial_data import GENERATE_SECURELY
from my_model.instance import Instance


def _valid() -> dict[str, object]:
    return {"user_id": 1, "name": "MetaTrader", "trading_platform_id": 1}


def test_valid_construction_succeeds() -> None:
    instance = Instance.model_validate(_valid())
    assert instance.status is True
    assert instance.password is None


def test_missing_required_field_is_rejected() -> None:
    data = _valid()
    del data["trading_platform_id"]
    with pytest.raises(ValidationError):
        Instance.model_validate(data)


def test_credential_fields_are_declared_sensitive_and_encrypted() -> None:
    schema = Instance.model_json_schema()
    for field in ("password", "api_key"):
        assert schema["properties"][field].get("credential") is True
        assert schema["properties"][field].get("storage_at_rest") == "encrypted"


def test_missing_required_connection_fields_reports_gaps() -> None:
    instance = Instance.model_validate(_valid())
    missing = instance.missing_required_connection_fields(
        ("ip", "username", "password")
    )
    assert missing == ("ip", "username", "password")


def test_missing_required_connection_fields_empty_when_all_present() -> None:
    instance = Instance.model_validate(
        {**_valid(), "ip": "127.0.0.1", "username": "test"}
    )
    missing = instance.missing_required_connection_fields(("ip", "username"))
    assert missing == ()


def test_uniqueness_rule_is_declared() -> None:
    assert Instance.UNIQUE_TOGETHER == (("user_id", "name"),)


def test_declared_initial_record_is_present() -> None:
    record = Instance.INITIAL_DATA[0]
    assert record["name"] == "MetaTrader"
    assert record["password"] is GENERATE_SECURELY
    assert record["api_key"] is GENERATE_SECURELY
