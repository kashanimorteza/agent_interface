"""Tests for Backend's Database Interface (task P3-G2-T1)."""

from __future__ import annotations

import time

import model
import pytest
from database import Database, TransactionConflict
from database.runtime_config import RuntimeConfig

from backend.database_interface import DatabaseInterface, PersistenceTimeout


def test_persistence_requests_reach_database_only_through_this_interface(
    test_db_config: RuntimeConfig,
) -> None:
    di = DatabaseInterface(
        Database(test_db_config, instance=test_db_config.default_instance),
        timeout_seconds=5.0,
        max_retry_attempts=3,
    )
    try:
        created = di.create(model.TradingPlatform(name="MetaTrader 5", code="metatrader_5"))
        assert di.get(model.TradingPlatform, created.id) is not None
    finally:
        di.close()


def test_grouped_operations_commit_or_roll_back_together(test_db_config: RuntimeConfig) -> None:
    di = DatabaseInterface(
        Database(test_db_config, instance=test_db_config.default_instance),
        timeout_seconds=5.0,
        max_retry_attempts=3,
    )
    try:
        with pytest.raises(RuntimeError):
            with di.transaction() as txn:
                di.create(model.TradingPlatform(name="MetaTrader 5", code="metatrader_5"), txn=txn)
                raise RuntimeError("fail the unit")
        assert di.list(model.TradingPlatform) == ()
    finally:
        di.close()


def test_deliberately_stalled_call_fails_after_its_finite_timeout(
    test_db_config: RuntimeConfig,
) -> None:
    di = DatabaseInterface(
        Database(test_db_config, instance=test_db_config.default_instance),
        timeout_seconds=0.05,
        max_retry_attempts=1,
    )
    try:

        def _slow(*_args: object, **_kwargs: object) -> None:
            time.sleep(1)

        with pytest.raises(PersistenceTimeout):
            di._call(_slow)
    finally:
        di.close()


def test_retry_is_bounded_and_stops_after_max_attempts(test_db_config: RuntimeConfig) -> None:
    di = DatabaseInterface(
        Database(test_db_config, instance=test_db_config.default_instance),
        timeout_seconds=5.0,
        max_retry_attempts=3,
    )
    attempts = {"count": 0}

    def _always_conflicts(*_args: object, **_kwargs: object) -> None:
        attempts["count"] += 1
        raise TransactionConflict("simulated conflict")

    try:
        with pytest.raises(TransactionConflict):
            di._call(_always_conflicts, retryable=True)
        assert attempts["count"] == 3
    finally:
        di.close()


def test_no_backend_source_imports_database_owned_connection_or_mapping_mechanism() -> None:
    import ast
    from pathlib import Path

    forbidden = {"StorageAdapter", "MAPPING_REGISTRY", "Base"}
    backend_src = Path(__file__).resolve().parents[1] / "src" / "backend"
    for path in backend_src.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module and "database" in node.module:
                imported = {alias.name for alias in node.names}
                assert not (imported & forbidden), f"{path} imports {imported & forbidden}"
