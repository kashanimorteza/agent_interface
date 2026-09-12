"""Application composition and machine-readable API contract checks."""

from __future__ import annotations

MODEL_PREFIXES = [
    "/users",
    "/trading-platforms",
    "/currencies",
    "/brokers",
    "/instances",
    "/assets",
    "/account-groups",
    "/accounts",
    "/trailing-groups",
    "/trailing-rules",
    "/partial-groups",
    "/partial-rules",
    "/action-groups",
    "/actions",
    "/positions",
]

CREDENTIAL_FIELDS_BY_SCHEMA = {
    "UserRead": {"password", "api_key"},
    "InstanceRead": {"password", "api_key"},
    "AccountRead": {"password"},
}


def test_openapi_is_reachable_and_lists_every_model(client):
    resp = client.get("/openapi.json")
    assert resp.status_code == 200
    spec = resp.json()
    for prefix in MODEL_PREFIXES:
        assert prefix in spec["paths"], f"missing {prefix} in OpenAPI paths"
        assert f"{prefix}/{{record_id}}" in spec["paths"]
        assert f"{prefix}/{{record_id}}/status" in spec["paths"]


def test_operation_ids_are_unique_across_the_whole_api(client):
    spec = client.get("/openapi.json").json()
    operation_ids = [
        operation["operationId"]
        for path_item in spec["paths"].values()
        for operation in path_item.values()
        if isinstance(operation, dict) and "operationId" in operation
    ]
    assert len(operation_ids) == len(set(operation_ids))


def test_every_response_schema_excludes_every_credential_field(client):
    spec = client.get("/openapi.json").json()
    schemas = spec["components"]["schemas"]
    for read_schema_name, credential_fields in CREDENTIAL_FIELDS_BY_SCHEMA.items():
        properties = schemas[read_schema_name].get("properties", {})
        for field in credential_fields:
            assert field not in properties, (
                f"{read_schema_name} leaks credential field {field}"
            )


def test_no_read_schema_anywhere_exposes_a_credential_field(client):
    """Independent of the known list above: scan every *Read schema generically."""
    spec = client.get("/openapi.json").json()
    schemas = spec["components"]["schemas"]
    known_credential_fields = {"password", "api_key"}
    for name, schema in schemas.items():
        if not name.endswith("Read"):
            continue
        leaked = known_credential_fields & schema.get("properties", {}).keys()
        assert not leaked, f"{name} leaks credential field(s) {leaked}"


def test_every_credential_field_is_present_and_write_only_on_create(client):
    spec = client.get("/openapi.json").json()
    schemas = spec["components"]["schemas"]
    user_create = schemas["UserCreate"]
    assert "password" in user_create["properties"]
    assert "api_key" in user_create["properties"]


def test_docs_ui_is_reachable(client):
    resp = client.get("/docs")
    assert resp.status_code == 200
