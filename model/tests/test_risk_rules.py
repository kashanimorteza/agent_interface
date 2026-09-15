"""Tests for Trailing Group, Trailing Rule, Partial Group, and Partial Rule."""

from decimal import Decimal

import pytest
from pydantic import ValidationError

from model.foundation import ForeignKey, persistence_contract
from model.partial_group import PartialGroup
from model.partial_rule import PartialRule
from model.trailing_group import TrailingGroup
from model.trailing_rule import TrailingRule


def test_trailing_group_relationship_and_uniqueness() -> None:
    group = TrailingGroup(user_id=1, name="Default")
    assert group.is_active is True
    contract = persistence_contract(TrailingGroup)
    by_name = {f.name: f.meta for f in contract.fields}
    assert by_name["user_id"].foreign_key == ForeignKey("User", "id")
    assert contract.unique_sets == (("user_id", "name"),)


def test_trailing_rule_relationship_optional_adjustments_and_uniqueness() -> None:
    rule = TrailingRule(name="R1", trailing_group_id=1, trigger_percentage=Decimal("50"))
    assert rule.take_profit_adjustment is None
    assert rule.stop_loss_adjustment is None

    contract = persistence_contract(TrailingRule)
    by_name = {f.name: f.meta for f in contract.fields}
    assert by_name["trailing_group_id"].foreign_key == ForeignKey("TrailingGroup", "id")
    assert by_name["name"].unique is True
    assert contract.unique_sets == (("trailing_group_id", "trigger_percentage"),)

    with pytest.raises(ValidationError):
        TrailingRule(name="R2", trailing_group_id=1)  # type: ignore[call-arg]


def test_partial_group_relationship_and_uniqueness() -> None:
    group = PartialGroup(user_id=1, name="Default")
    assert group.is_active is True
    contract = persistence_contract(PartialGroup)
    assert contract.unique_sets == (("user_id", "name"),)


def test_partial_rule_relationship_and_uniqueness() -> None:
    rule = PartialRule(
        name="R1",
        partial_group_id=1,
        profit_percentage=Decimal("25"),
        close_percentage=Decimal("50"),
    )
    assert rule.is_active is True

    contract = persistence_contract(PartialRule)
    by_name = {f.name: f.meta for f in contract.fields}
    assert by_name["partial_group_id"].foreign_key == ForeignKey("PartialGroup", "id")
    assert contract.unique_sets == (("partial_group_id", "profit_percentage"),)
