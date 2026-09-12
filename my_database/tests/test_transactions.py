"""The transaction boundary (Task P2-T7)."""

from __future__ import annotations

import my_model as m
import pytest

import my_database as db
from my_database.exceptions import DatabaseError


def test_successful_group_commits_together():
    with db.transactions.unit(instance="general") as tx:
        first = db.operations.add(m.AccountGroup, unit=tx, user_id=1, name="TxCommitA")
        second = db.operations.add(m.AccountGroup, unit=tx, user_id=1, name="TxCommitB")

    assert db.operations.get(m.AccountGroup, first.id, instance="general").name == "TxCommitA"
    assert db.operations.get(m.AccountGroup, second.id, instance="general").name == "TxCommitB"


def test_failed_group_leaves_no_partial_change():
    before = len(db.operations.list(m.AccountGroup, instance="general"))
    with pytest.raises(DatabaseError):
        with db.transactions.unit(instance="general") as tx:
            db.operations.add(m.AccountGroup, unit=tx, user_id=1, name="TxRollback")
            db.operations.add(
                m.AccountGroup, unit=tx, user_id=1, name="TxRollback"
            )  # duplicate name

    after = len(db.operations.list(m.AccountGroup, instance="general"))
    assert after == before
    assert db.operations.list(m.AccountGroup, instance="general", name="TxRollback") == []
