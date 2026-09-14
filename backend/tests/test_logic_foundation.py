"""Tests for the Logic Foundation (task P3-G3-T1)."""

from __future__ import annotations

import model
import pytest

from backend.database_interface import DatabaseInterface
from backend.logic.foundation import ModelLogicBase
from backend.logic.outcomes import ConflictOutcome, NotFound, ValidationFailed


class _UserLogicForTest(ModelLogicBase[model.User]):
    model_cls = model.User


class _PlatformLogicForTest(ModelLogicBase[model.TradingPlatform]):
    model_cls = model.TradingPlatform


def _di(db) -> DatabaseInterface:
    return DatabaseInterface(db, timeout_seconds=5.0, max_retry_attempts=3)


def test_standard_operations_behave_consistently_across_more_than_one_unit(db) -> None:
    di = _di(db)
    user_logic = _UserLogicForTest(di)
    platform_logic = _PlatformLogicForTest(di)

    user = user_logic.create({"name": "Ada", "username": "ada", "password": "pw", "api_key": "key"})
    platform = platform_logic.create({"name": "MetaTrader 5", "code": "metatrader_5"})

    assert user_logic.get_by_id(user.id).name == "Ada"
    assert platform_logic.get_by_id(platform.id).name == "MetaTrader 5"

    assert user_logic.disable(user.id).is_active is False
    assert platform_logic.disable(platform.id).is_active is False


def test_get_by_id_raises_not_found_for_missing_record(db) -> None:
    logic = _UserLogicForTest(_di(db))
    with pytest.raises(NotFound):
        logic.get_by_id(999)


def test_create_raises_validation_failed_for_invalid_data(db) -> None:
    logic = _UserLogicForTest(_di(db))
    with pytest.raises(ValidationFailed):
        logic.create({"name": "Ada"})  # missing required fields


def test_create_raises_conflict_outcome_on_uniqueness_violation(db) -> None:
    logic = _UserLogicForTest(_di(db))
    logic.create({"name": "Ada", "username": "ada", "password": "pw", "api_key": "key"})
    with pytest.raises(ConflictOutcome):
        logic.create({"name": "Ada", "username": "ada2", "password": "x", "api_key": "y"})


def test_update_merges_partial_data_and_preserves_unspecified_fields(db) -> None:
    logic = _UserLogicForTest(_di(db))
    user = logic.create({"name": "Ada", "username": "ada", "password": "pw", "api_key": "key"})
    updated = logic.update(user.id, {"description": "engineer"})
    assert updated.description == "engineer"
    assert updated.username == "ada"


def test_delete_is_exposed_by_the_foundation(db) -> None:
    logic = _PlatformLogicForTest(_di(db))
    platform = logic.create({"name": "Kraken", "code": "kraken"})
    assert logic.delete(platform.id) is None
    with pytest.raises(NotFound):
        logic.get_by_id(platform.id)
