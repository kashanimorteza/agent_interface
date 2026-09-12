"""Model validation check: valid state, invalid state, boundary values,
nullability, defaults, and omitted vs. explicit-null semantics.
"""

from decimal import Decimal
from types import ModuleType

import pytest
from pydantic import ValidationError

import my_model


def test_valid_user_construction() -> None:
    u = my_model.User(id=1, name="Admin", username="admin", password="x", api_key="y")
    assert u.status is True
    assert u.description is None


def test_user_rejects_missing_required_field() -> None:
    with pytest.raises(ValidationError):
        my_model.User(id=1, name="Admin", username="admin", password="x")


def test_user_rejects_unknown_field() -> None:
    with pytest.raises(ValidationError):
        my_model.User.model_validate(
            {
                "id": 1,
                "name": "Admin",
                "username": "admin",
                "password": "x",
                "api_key": "y",
                "unknown": "value",
            }
        )


def test_user_credential_fields_are_declared_hash() -> None:
    for field_name in ("password", "api_key"):
        extra = my_model.User.model_fields[field_name].json_schema_extra
        assert extra == {"credential": True, "storage_at_rest": "hash"}


def test_instance_credential_fields_are_declared_encrypted_and_optional() -> None:
    for field_name in ("password", "api_key"):
        field = my_model.Instance.model_fields[field_name]
        assert field.json_schema_extra == {"credential": True, "storage_at_rest": "encrypted"}
        assert field.default is None

    instance = my_model.Instance(id=1, user_id=1, name="MT", trading_platform_id=1)
    assert instance.password is None
    assert instance.api_key is None


def test_account_credential_field_is_declared_encrypted() -> None:
    extra = my_model.Account.model_fields["password"].json_schema_extra
    assert extra == {"credential": True, "storage_at_rest": "encrypted"}


def test_currency_code_boundary_length() -> None:
    my_model.Currency(id=1, user_id=1, code="USD")
    with pytest.raises(ValidationError):
        my_model.Currency(id=1, user_id=1, code="US")
    with pytest.raises(ValidationError):
        my_model.Currency(id=1, user_id=1, code="USDD")


def test_currency_default_decimal_digits() -> None:
    c = my_model.Currency(id=1, user_id=1, code="USD")
    assert c.decimal_digits == 2


def test_omitted_optional_field_and_explicit_none_are_both_valid_and_equal() -> None:
    omitted = my_model.Broker(id=1, name="FxPro", user_id=1)
    explicit_none = my_model.Broker(id=1, name="FxPro", user_id=1, description=None)
    assert omitted.description is None
    assert explicit_none.description is None
    assert omitted == explicit_none


def test_explicit_false_and_zero_are_preserved_over_defaults() -> None:
    inactive_asset = my_model.Asset(
        id=1, broker_id=1, symbol="EUR/USD", category="Currency", point_size=0.0, digits=0,
        status=False,
    )
    assert inactive_asset.status is False
    assert inactive_asset.point_size == 0.0
    assert inactive_asset.digits == 0


def test_partial_update_preserves_omission_vs_replacement_semantics() -> None:
    original = my_model.TrailingRule(
        id=1,
        name="Trigger 50%",
        trailing_group_id=1,
        trigger_percentage=Decimal(50),
        take_profit_adjustment=Decimal(1),
    )
    partial_update = {"stop_loss_adjustment": Decimal(2)}
    updated = original.model_copy(update=partial_update)
    # Field omitted from the update keeps its current value.
    assert updated.take_profit_adjustment == Decimal(1)
    # Field supplied in the update replaces the current value.
    assert updated.stop_loss_adjustment == Decimal(2)


def test_decimal_precision_is_exact_for_financial_fields() -> None:
    action = my_model.Action(
        id=1,
        name="Default",
        action_group_id=1,
        asset_id=1,
        account_id=1,
        partial_group_id=1,
        trailing_group_id=1,
        risk_by_reward=Decimal("1.1"),
        take_profit=Decimal("1.2345"),
        stop_loss=Decimal("0.9999"),
    )
    assert action.take_profit == Decimal("1.2345")
    assert isinstance(action.take_profit, Decimal)


def test_position_requires_every_declared_field() -> None:
    with pytest.raises(ValidationError):
        my_model.Position.model_validate({"id": 1, "user_id": 1, "name": "P1"})


@pytest.mark.parametrize(
    "module",
    [
        my_model.user,
        my_model.trading_platform,
        my_model.instance,
        my_model.currency,
        my_model.broker,
        my_model.asset,
        my_model.account_group,
        my_model.account,
        my_model.trailing_group,
        my_model.partial_group,
        my_model.action_group,
        my_model.action,
    ],
)
def test_declared_initial_data_is_a_list_of_mappings(module: ModuleType) -> None:
    initial_data = module.INITIAL_DATA
    assert isinstance(initial_data, list)
    assert len(initial_data) > 0
    for record in initial_data:
        assert isinstance(record, dict)


@pytest.mark.parametrize("module", [my_model.trailing_rule, my_model.partial_rule, my_model.position])
def test_models_without_declared_initial_data_have_none(module: ModuleType) -> None:
    assert not hasattr(module, "INITIAL_DATA")


def test_generated_fields_are_absent_from_initial_data() -> None:
    for record in my_model.user.INITIAL_DATA:
        assert "id" not in record
        assert "password" not in record
        assert "api_key" not in record

    for record in my_model.instance.INITIAL_DATA:
        assert "password" not in record
        assert "api_key" not in record

    for record in my_model.account.INITIAL_DATA:
        assert "password" not in record
