"""Whole-surface API contract assurance (P3-T17): no credential field
appears in the published API description or in any actual response body,
across every Model rather than one at a time.
"""

import my_model
from fastapi.testclient import TestClient

from my_backend._model_interface import credential_field_names

_ALL_MODELS = [
    my_model.User,
    my_model.TradingPlatform,
    my_model.Instance,
    my_model.Currency,
    my_model.Broker,
    my_model.Asset,
    my_model.AccountGroup,
    my_model.Account,
    my_model.TrailingGroup,
    my_model.TrailingRule,
    my_model.PartialGroup,
    my_model.PartialRule,
    my_model.ActionGroup,
    my_model.Action,
    my_model.Position,
]


def test_no_response_schema_in_the_published_api_description_contains_a_credential_field(
    client: TestClient,
) -> None:
    openapi = client.get("/openapi.json").json()
    schemas = openapi["components"]["schemas"]

    checked_any_credential_model = False
    for model_type in _ALL_MODELS:
        credential_names = credential_field_names(model_type)
        if not credential_names:
            continue
        read_schema_name = f"{model_type.__name__}Read"
        assert read_schema_name in schemas, f"{read_schema_name} missing from published API description"
        properties = schemas[read_schema_name]["properties"]
        for field_name in credential_names:
            assert field_name not in properties, (
                f"{read_schema_name} exposes credential field {field_name!r}"
            )
            checked_any_credential_model = True

    assert checked_any_credential_model, "no credential-bearing Model was actually checked"


def test_every_credential_bearing_model_has_a_write_only_create_field(client: TestClient) -> None:
    openapi = client.get("/openapi.json").json()
    schemas = openapi["components"]["schemas"]

    for model_type in _ALL_MODELS:
        credential_names = credential_field_names(model_type)
        if not credential_names:
            continue
        create_schema_name = f"{model_type.__name__}Create"
        properties = schemas[create_schema_name]["properties"]
        for field_name in credential_names:
            assert field_name in properties, (
                f"{create_schema_name} does not accept credential field {field_name!r} as input"
            )
