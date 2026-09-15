"""Verifies P2T2: physical storage structure derived from Model's published metadata."""

from __future__ import annotations

from model import Account, Instance, User
from model.foundation import DomainModel
from sqlalchemy import UniqueConstraint

from database.mapping import ALL_MODELS, table_for


class _NonPersistent(DomainModel):
    __persistent__ = False
    id: int | None = None


def test_every_persistent_model_produces_a_table_matching_its_metadata() -> None:
    for model_cls in ALL_MODELS:
        table = table_for(model_cls)
        meta = model_cls.persistence_metadata()
        assert table is not None
        column_names = {c.name for c in table.columns}
        assert column_names == set(meta["fields"])
        for field_name, field_meta in meta["fields"].items():
            column = table.columns[field_name]
            assert column.primary_key == field_meta["primary_key"]
            assert column.nullable == field_meta["nullable"]


def test_foreign_keys_reference_the_correct_table_and_column() -> None:
    table = table_for(Instance)
    assert table is not None
    fk_targets = {fk.target_fullname for fk in table.columns["user_id"].foreign_keys}
    assert fk_targets == {"users.id"}
    fk_targets_platform = {
        fk.target_fullname for fk in table.columns["trading_platform_id"].foreign_keys
    }
    assert fk_targets_platform == {"trading_platforms.id"}


def test_composite_unique_sets_become_table_constraints() -> None:
    table = table_for(Account)
    assert table is not None
    constraint_columns = [
        tuple(c.name for c in uc.columns)
        for uc in table.constraints
        if isinstance(uc, UniqueConstraint) and len(uc.columns) > 1
    ]
    assert ("group_id", "broker_id", "instance_id") in constraint_columns


def test_single_field_unique_metadata_becomes_column_unique() -> None:
    table = table_for(User)
    assert table is not None
    assert table.columns["name"].unique is True
    assert table.columns["username"].unique is True


def test_non_persistent_model_produces_no_table() -> None:
    assert table_for(_NonPersistent) is None
