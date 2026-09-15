from decimal import Decimal

from conftest import (
    assert_rejects_unknown_field,
    assert_requires_field,
    assert_serializes_and_generates_schema,
)

from model import Action

VALID = {
    "name": "Default",
    "action_group_id": 1,
    "asset_id": 1,
    "account_id": 1,
    "partial_group_id": 1,
    "trailing_group_id": 1,
    "risk_by_reward": Decimal(1),
    "take_profit": Decimal(1),
    "stop_loss": Decimal(1),
}


def test_valid_construction_applies_declared_defaults():
    action = Action.model_validate(VALID)
    assert action.is_active is True


def test_rejects_unknown_field():
    assert_rejects_unknown_field(Action, VALID)


def test_requires_declared_non_nullable_fields():
    for field in (
        "name",
        "action_group_id",
        "asset_id",
        "account_id",
        "partial_group_id",
        "trailing_group_id",
        "risk_by_reward",
        "take_profit",
        "stop_loss",
    ):
        assert_requires_field(Action, VALID, field)


def test_publishes_relationships_and_uniqueness_metadata():
    contract = Action.persistence_contract()
    assert contract.fields["name"].unique is False
    assert ("action_group_id", "name") in contract.unique_sets
    references = {r.field: r.references for r in contract.relationships}
    assert references == {
        "action_group_id": "ActionGroup",
        "asset_id": "Asset",
        "account_id": "Account",
        "partial_group_id": "PartialGroup",
        "trailing_group_id": "TrailingGroup",
    }


def test_serializes_and_generates_schema():
    assert_serializes_and_generates_schema(Action.model_validate(VALID))
