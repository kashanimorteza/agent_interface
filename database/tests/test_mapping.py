from __future__ import annotations

import model

from database.mapping import MAPPINGS, TABLES

ALL_DOMAIN_DEFINITIONS = [
    model.User,
    model.TradingPlatform,
    model.Broker,
    model.Instance,
    model.Currency,
    model.Asset,
    model.AccountGroup,
    model.Account,
    model.TrailingGroup,
    model.TrailingRule,
    model.PartialGroup,
    model.PartialRule,
    model.ActionGroup,
    model.Action,
    model.Position,
]


def test_every_domain_definition_has_a_traceable_mapping() -> None:
    for model_cls in ALL_DOMAIN_DEFINITIONS:
        assert model_cls in MAPPINGS, f"{model_cls.__name__} has no ModelMapping"
        assert model_cls in TABLES, f"{model_cls.__name__} has no built Table"


def test_mapped_table_columns_match_domain_definition_fields() -> None:
    for model_cls in ALL_DOMAIN_DEFINITIONS:
        table = TABLES[model_cls]
        assert set(table.c.keys()) == set(model_cls.model_fields.keys())


def test_id_is_the_primary_key_for_every_mapping() -> None:
    for model_cls in ALL_DOMAIN_DEFINITIONS:
        table = TABLES[model_cls]
        assert [c.name for c in table.primary_key.columns] == ["id"]


def test_declared_uniqueness_constraints_are_present() -> None:
    expected = {
        "users": {("name",)},
        "trading_platforms": set(),
        "brokers": {("user_id", "name")},
        "instances": {("user_id", "name")},
        "currencies": {("user_id", "code")},
        "assets": {("broker_id", "symbol")},
        "account_groups": {("user_id", "name")},
        "accounts": {("name",), ("group_id", "broker_id", "instance_id")},
        "trailing_groups": {("user_id", "name")},
        "trailing_rules": {("name",), ("trailing_group_id", "trigger_percentage")},
        "partial_groups": {("user_id", "name")},
        "partial_rules": {("name",), ("partial_group_id", "profit_percentage")},
        "action_groups": {("user_id", "name")},
        "actions": {("action_group_id", "name")},
        "positions": {("name",)},
    }
    for model_cls in ALL_DOMAIN_DEFINITIONS:
        table = TABLES[model_cls]
        found = {
            tuple(col.name for col in constraint.columns)
            for constraint in table.constraints
            if constraint.__class__.__name__ == "UniqueConstraint"
        }
        assert found == expected[table.name], f"{table.name}: {found} != {expected[table.name]}"


def test_foreign_keys_reference_the_expected_tables() -> None:
    table = TABLES[model.Account]
    fk_targets = {fk.parent.name: fk.column.table.name for fk in table.foreign_keys}
    assert fk_targets == {
        "group_id": "account_groups",
        "broker_id": "brokers",
        "instance_id": "instances",
        "base_currency_id": "currencies",
    }
