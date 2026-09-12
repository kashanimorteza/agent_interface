"""Data Access: the sole Backend boundary consuming Database, and its
transaction grouping (Task P3-T2).
"""

from __future__ import annotations

from pathlib import Path

import my_model as m
import pytest

from backend import data_access


def test_create_get_update_delete_reach_the_correct_database_operation_for_multiple_models():
    broker = data_access.create(m.Broker, name="DataAccessBrokerA", user_id=1)
    currency = data_access.create(m.Currency, user_id=1, code="DA1")
    assert broker.id is not None
    assert currency.id is not None

    assert data_access.get(m.Broker, broker.id).name == "DataAccessBrokerA"
    assert data_access.get(m.Currency, currency.id).code == "DA1"

    updated = data_access.update(m.Broker, broker.id, description="updated")
    assert updated.description == "updated"

    data_access.delete(m.Broker, broker.id)
    with pytest.raises(data_access.NotFound):
        data_access.get(m.Broker, broker.id)


def test_transaction_commits_a_group_together():
    with data_access.transaction() as tx:
        a = data_access.create(m.AccountGroup, unit=tx, user_id=1, name="DATxGroupA")
        b = data_access.create(m.AccountGroup, unit=tx, user_id=1, name="DATxGroupB")
    assert a.id is not None
    assert b.id is not None

    assert data_access.get(m.AccountGroup, a.id).name == "DATxGroupA"
    assert data_access.get(m.AccountGroup, b.id).name == "DATxGroupB"


def test_transaction_rolls_back_a_failed_group():
    before = len(data_access.list_records(m.AccountGroup))
    with pytest.raises(data_access.DatabaseError):
        with data_access.transaction() as tx:
            data_access.create(m.AccountGroup, unit=tx, user_id=1, name="DATxFail")
            data_access.create(m.AccountGroup, unit=tx, user_id=1, name="DATxFail")

    after = len(data_access.list_records(m.AccountGroup))
    assert after == before
    assert data_access.list_records(m.AccountGroup, name="DATxFail") == []


def test_only_data_access_module_imports_my_database():
    src_root = Path(__file__).resolve().parent.parent / "src" / "backend"
    offenders = []
    for path in src_root.rglob("*.py"):
        if path.name == "data_access.py":
            continue
        text = path.read_text()
        if "import my_database" in text or "from my_database" in text:
            offenders.append(str(path))
    assert offenders == []
