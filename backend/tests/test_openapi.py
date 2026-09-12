"""The published machine-readable API description (Task P3-T5)."""

from __future__ import annotations


def test_openapi_covers_every_resource(client):
    schema = client.get("/openapi.json").json()
    resources = {path.strip("/").split("/")[0] for path in schema["paths"] if path.strip("/")}
    assert resources == {
        "users",
        "trading-platforms",
        "instances",
        "currencies",
        "brokers",
        "assets",
        "account-groups",
        "accounts",
        "trailing-groups",
        "trailing-rules",
        "partial-groups",
        "partial-rules",
        "action-groups",
        "actions",
        "positions",
    }


def test_no_read_schema_exposes_a_credential_field(client):
    schema = client.get("/openapi.json").json()
    for name, component in schema["components"]["schemas"].items():
        if name.endswith("Read"):
            properties = component.get("properties", {})
            assert "password" not in properties, name
            assert "api_key" not in properties, name


def test_create_schema_accepts_credential_fields_as_write_only_input(client):
    schema = client.get("/openapi.json").json()
    user_create = schema["components"]["schemas"]["UserCreate"]
    assert "password" in user_create["properties"]
    assert "api_key" in user_create["properties"]
    assert "password" in user_create.get("required", [])
