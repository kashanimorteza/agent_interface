"""Tests for the machine-readable API contract (task P3-G10-T2)."""

from __future__ import annotations

from backend.logic.registry import LOGIC_REGISTRY


def test_contract_describes_every_exposed_model_logic_units_operations(client) -> None:
    schema = client.get("/openapi.json").json()
    paths = schema["paths"]

    for logic_cls in LOGIC_REGISTRY:
        import re

        words = re.findall(r"[A-Z][a-z0-9]*", logic_cls.model_cls.__name__)
        segment = "-".join(w.lower() for w in words)
        base_path = f"/v1/{segment}"
        assert base_path in paths, f"missing {base_path}"
        assert "post" in paths[base_path]
        assert "get" in paths[base_path]
        assert f"{base_path}/{{item_id}}" in paths
        assert "get" in paths[f"{base_path}/{{item_id}}"]
        assert "put" in paths[f"{base_path}/{{item_id}}"]


def test_contract_version_matches_configured_api_version(client, settings) -> None:
    schema = client.get("/openapi.json").json()
    assert schema["info"]["version"] == settings.api_version


def test_no_credential_value_present_in_the_published_contract(client) -> None:
    schema = client.get("/openapi.json").json()
    text = str(schema)
    assert "***protected***" not in text
    # Credential fields (password, api_key) never appear in a *response* (output) schema.
    for name, definition in schema.get("components", {}).get("schemas", {}).items():
        if name.endswith("Read"):
            assert "password" not in definition.get("properties", {})
            assert "api_key" not in definition.get("properties", {})
