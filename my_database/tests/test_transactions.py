"""The explicit transaction boundary."""

import my_model
import pytest

import my_database


def test_a_fully_successful_group_commits_every_change_together() -> None:
    user = my_database.add(
        my_model.User(id=0, name="Admin", username="admin", password="x", api_key="y")
    )
    with my_database.transaction() as session:
        my_database.add(my_model.Broker(id=0, name="FxPro", user_id=user.id), session=session)
        my_database.add(my_model.Broker(id=0, name="FxPro2", user_id=user.id), session=session)

    names = {b.name for b in my_database.list_records(my_model.Broker)}
    assert names == {"FxPro", "FxPro2"}


def test_a_failing_group_rolls_back_every_change_it_made() -> None:
    user = my_database.add(
        my_model.User(id=0, name="Admin", username="admin", password="x", api_key="y")
    )
    with pytest.raises(my_database.errors.ConstraintViolationError), my_database.transaction() as session:
        my_database.add(my_model.Broker(id=0, name="FxPro", user_id=user.id), session=session)
        my_database.add(my_model.Broker(id=0, name="Bad", user_id=999999), session=session)

    assert my_database.list_records(my_model.Broker) == []


def test_a_standalone_operation_outside_any_group_commits_independently() -> None:
    created = my_database.add(
        my_model.User(id=0, name="Admin", username="admin", password="x", api_key="y")
    )
    fetched = my_database.read(my_model.User, created.id)
    assert fetched.id == created.id
