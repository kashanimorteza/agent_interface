from __future__ import annotations

import model

from database.mapping import METADATA, contract_for, table_for


def test_every_persistent_model_is_mapped() -> None:
    assert len(METADATA.tables) == 15


def test_mapping_preserves_primary_key_and_foreign_keys() -> None:
    users = table_for(model.User)
    assert users.c.id.primary_key

    instances = table_for(model.Instance)
    fk_targets = {fk.target_fullname for col in instances.columns for fk in col.foreign_keys}
    assert "users.id" in fk_targets
    assert "trading_platforms.id" in fk_targets


def test_mapping_preserves_composite_uniqueness() -> None:
    accounts = table_for(model.Account)
    unique_constraints = [c for c in accounts.constraints if c.__class__.__name__ == "UniqueConstraint"]
    composite = {tuple(sorted(col.name for col in uc.columns)) for uc in unique_constraints}
    assert tuple(sorted(("group_id", "broker_id", "instance_id"))) in composite


def test_mapping_matches_published_persistence_contract_exactly() -> None:
    for cls in (model.User, model.Instance, model.Account, model.Position):
        contract = contract_for(cls)
        table = table_for(cls)
        assert {f.name for f in contract.fields} == {c.name for c in table.columns}
        for field in contract.fields:
            column = table.c[field.name]
            assert column.nullable == field.meta.nullable
            assert bool(column.primary_key) == field.meta.primary_key
