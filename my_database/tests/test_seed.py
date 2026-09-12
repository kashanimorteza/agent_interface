"""Initial-data seeding (Task P2-T8)."""

from __future__ import annotations

import my_model as m

import my_database as db


def test_seed_populates_every_declared_initial_record(seeded_database):
    assert seeded_database["User"] == 1
    assert seeded_database["TradingPlatform"] == 2
    assert seeded_database["Currency"] == 8
    assert seeded_database["Broker"] == 1
    assert seeded_database["Account"] == 1
    assert seeded_database["Action"] == 1


def test_seed_is_idempotent():
    """Seeding twice must not duplicate any Model-declared initial record,
    regardless of unrelated records other tests may have added in between.
    """
    second_run = db.seed(instance="general")
    assert all(count == 0 for count in second_run.values())
    assert len(db.operations.list(m.User, instance="general", name="Admin")) == 1
    assert len(db.operations.list(m.Currency, instance="general", code="USD")) == 1


def test_seeded_relationships_resolve_correctly():
    (account,) = db.operations.list(m.Account, instance="general", name="Acc-1")
    group = db.operations.get(m.AccountGroup, account.group_id, instance="general")
    broker = db.operations.get(m.Broker, account.broker_id, instance="general")
    assert group.name == "Default"
    assert broker.name == "FxPro"
