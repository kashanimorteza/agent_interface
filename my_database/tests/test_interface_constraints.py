from __future__ import annotations

import pytest
from my_model.broker import Broker
from my_model.currency import Currency
from my_model.user import User

from my_database import interface


def _make_user() -> User:
    user = interface.add(User(name="Ada", username="ada", password="x", api_key="y"))
    assert user.id is not None
    return user


def test_uniqueness_constraint_is_enforced_at_persistence():
    user = _make_user()
    assert user.id is not None
    interface.add(Broker(name="FxPro", user_id=user.id))
    with pytest.raises(interface.ConstraintViolationError):
        interface.add(Broker(name="FxPro", user_id=user.id))


def test_reference_to_nonexistent_record_is_rejected():
    with pytest.raises(interface.ConstraintViolationError):
        interface.add(Currency(user_id=999, code="USD"))


def test_transaction_rolls_back_every_operation_on_failure():
    user = _make_user()
    assert user.id is not None
    with (
        pytest.raises(interface.ConstraintViolationError),
        interface.transaction() as txn,
    ):
        interface.add(Broker(name="Unique-1", user_id=user.id), within=txn)
        interface.add(
            Broker(name="Unique-1", user_id=user.id), within=txn
        )  # duplicate -> fails

    # Nothing from the failed transaction is visible.
    assert interface.list_(Broker, name="Unique-1") == []


def test_transaction_commits_every_operation_together_on_success():
    user = _make_user()
    assert user.id is not None
    with interface.transaction() as txn:
        interface.add(Broker(name="Group-A", user_id=user.id), within=txn)
        interface.add(Broker(name="Group-B", user_id=user.id), within=txn)

    assert len(interface.list_(Broker, user_id=user.id)) == 2
