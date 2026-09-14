from decimal import Decimal

from model import PartialGroup, PartialRule, TrailingGroup, TrailingRule


def test_trailing_group_accepts_valid_data():
    group = TrailingGroup(user_id=1, name="Default")
    assert group.is_active is True


def test_trailing_group_declares_per_user_name_uniqueness_metadata():
    assert TrailingGroup.unique_together == (("user_id", "name"),)


def test_trailing_rule_accepts_valid_data_with_optional_adjustments_omitted():
    rule = TrailingRule(
        name="TR-1", trailing_group_id=1, trigger_percentage=Decimal(50)
    )
    assert rule.take_profit_adjustment is None
    assert rule.stop_loss_adjustment is None


def test_trailing_rule_declares_name_and_group_trigger_uniqueness_metadata():
    assert TrailingRule.unique_together == (
        ("name",),
        ("trailing_group_id", "trigger_percentage"),
    )


def test_partial_group_accepts_valid_data():
    group = PartialGroup(user_id=1, name="Default")
    assert group.is_active is True


def test_partial_group_declares_per_user_name_uniqueness_metadata():
    assert PartialGroup.unique_together == (("user_id", "name"),)


def test_partial_rule_accepts_valid_data():
    rule = PartialRule(
        name="PR-1",
        partial_group_id=1,
        profit_percentage=Decimal(50),
        close_percentage=Decimal(50),
    )
    assert rule.is_active is True


def test_partial_rule_declares_name_and_group_profit_uniqueness_metadata():
    assert PartialRule.unique_together == (
        ("name",),
        ("partial_group_id", "profit_percentage"),
    )
