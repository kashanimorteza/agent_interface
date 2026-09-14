"""Tests for the Trade Management Rule storage mappings (tasks P2-G6-T1..T4)."""

from __future__ import annotations

from decimal import Decimal

import model
import pytest

from database.exceptions import ConstraintViolation


def test_trailing_group_mapping_preserves_fields_relationship_and_uniqueness(db) -> None:
    user = db.create(model.User(name="Ada", username="ada", password="pw", api_key="key"))
    created = db.create(model.TrailingGroup(user_id=user.id, name="Default"))
    fetched = db.get(model.TrailingGroup, created.id)
    assert fetched is not None
    assert fetched.name == "Default"

    with pytest.raises(ConstraintViolation):
        db.create(model.TrailingGroup(user_id=user.id, name="Default"))


def test_trailing_rule_mapping_preserves_fields_relationship_and_uniqueness(db) -> None:
    user = db.create(model.User(name="Ada", username="ada", password="pw", api_key="key"))
    group = db.create(model.TrailingGroup(user_id=user.id, name="Default"))
    created = db.create(
        model.TrailingRule(
            name="Rule-1", trailing_group_id=group.id, trigger_percentage=Decimal("50")
        )
    )
    fetched = db.get(model.TrailingRule, created.id)
    assert fetched is not None
    assert fetched.trailing_group_id == group.id
    assert fetched.trigger_percentage == Decimal("50")

    with pytest.raises(ConstraintViolation):
        db.create(
            model.TrailingRule(
                name="Rule-2", trailing_group_id=group.id, trigger_percentage=Decimal("50")
            )
        )


def test_partial_group_mapping_preserves_fields_relationship_and_uniqueness(db) -> None:
    user = db.create(model.User(name="Ada", username="ada", password="pw", api_key="key"))
    created = db.create(model.PartialGroup(user_id=user.id, name="Default"))
    fetched = db.get(model.PartialGroup, created.id)
    assert fetched is not None
    assert fetched.name == "Default"

    with pytest.raises(ConstraintViolation):
        db.create(model.PartialGroup(user_id=user.id, name="Default"))


def test_partial_rule_mapping_preserves_fields_relationship_and_uniqueness(db) -> None:
    user = db.create(model.User(name="Ada", username="ada", password="pw", api_key="key"))
    group = db.create(model.PartialGroup(user_id=user.id, name="Default"))
    created = db.create(
        model.PartialRule(
            name="Rule-1",
            partial_group_id=group.id,
            profit_percentage=Decimal("25"),
            close_percentage=Decimal("50"),
        )
    )
    fetched = db.get(model.PartialRule, created.id)
    assert fetched is not None
    assert fetched.partial_group_id == group.id
    assert fetched.profit_percentage == Decimal("25")

    with pytest.raises(ConstraintViolation):
        db.create(
            model.PartialRule(
                name="Rule-2",
                partial_group_id=group.id,
                profit_percentage=Decimal("25"),
                close_percentage=Decimal("75"),
            )
        )
