"""Verifies the generic Model-to-storage mapping mechanism."""

from __future__ import annotations

from database.mapping import (
    PERSISTENT_MODELS,
    build_metadata,
    portability_report,
    table_name,
)


def test_every_persistent_model_produces_a_table() -> None:
    metadata = build_metadata()
    for model_cls in PERSISTENT_MODELS:
        assert table_name(model_cls) in metadata.tables


def test_table_columns_trace_to_persistence_contract() -> None:
    from model import Account

    metadata = build_metadata()
    table = metadata.tables[table_name(Account)]
    contract = Account.persistence_contract()
    assert set(table.columns.keys()) == set(contract["fields"].keys())


def test_foreign_keys_resolve_to_correct_referenced_table() -> None:
    from model import Instance

    metadata = build_metadata()
    table = metadata.tables[table_name(Instance)]
    fk_targets = {
        fk.target_fullname for col in table.columns for fk in col.foreign_keys
    }
    assert "users.id" in fk_targets
    assert "trading_platforms.id" in fk_targets


def test_composite_unique_set_applied_to_table() -> None:
    from model import Account
    from sqlalchemy import UniqueConstraint

    metadata = build_metadata()
    table = metadata.tables[table_name(Account)]
    unique_constraints = [
        c for c in table.constraints if isinstance(c, UniqueConstraint)
    ]
    column_sets = [{c.name for c in uc.columns} for uc in unique_constraints]
    assert {"group_id", "broker_id", "instance_id"} in column_sets


def test_portability_report_classifies_every_entry() -> None:
    valid_classifications = {
        "portable_contract",
        "portable_mapping",
        "engine_specific_extension",
    }
    notes = portability_report()
    assert len(notes) > 0
    for note in notes:
        assert note.classification in valid_classifications
        assert note.subject
        assert note.note


def test_portability_report_isolates_sqlite_specific_decisions() -> None:
    notes = portability_report()
    engine_specific = [
        n for n in notes if n.classification == "engine_specific_extension"
    ]
    assert any(
        "SQLite" in n.subject or "sqlite" in n.note.lower() for n in engine_specific
    )
