"""Generic Model-driven data-access pipeline: add, read, list, edit, delete,
status, and their distinguishable failure outcomes.
"""

import my_model
import pytest
from pydantic import ValidationError

import my_database
from my_database import _credentials


def _make_user(**overrides: object) -> my_model.User:
    fields = {
        "id": 0,
        "name": "Admin",
        "username": "admin",
        "password": "x",
        "api_key": "y",
    }
    fields.update(overrides)
    return my_model.User(**fields)


def test_add_assigns_a_real_identity_and_ignores_the_placeholder() -> None:
    created = my_database.add(_make_user())
    assert created.id != 0
    assert isinstance(created.id, int)


def test_round_trip_preserves_every_declared_field() -> None:
    created = my_database.add(_make_user(description="a note"))
    fetched = my_database.read(my_model.User, created.id)
    assert fetched.name == "Admin"
    assert fetched.username == "admin"
    assert fetched.description == "a note"
    assert fetched.status is True


def test_read_missing_identifier_raises_not_found() -> None:
    with pytest.raises(my_database.errors.NotFoundError):
        my_database.read(my_model.User, 999999)


def test_list_returns_every_persisted_record() -> None:
    my_database.add(_make_user(name="Admin"))
    my_database.add(_make_user(name="Second", username="second"))
    records = my_database.list_records(my_model.User)
    assert {record.name for record in records} == {"Admin", "Second"}


def test_edit_replaces_supplied_fields_and_preserves_omitted_ones() -> None:
    created = my_database.add(_make_user(description="original"))
    edited = my_database.edit(my_model.User, created.id, {"description": "updated"})
    assert edited.description == "updated"
    assert edited.name == created.name  # omitted from the patch: unchanged


def test_edit_missing_identifier_raises_not_found() -> None:
    with pytest.raises(my_database.errors.NotFoundError):
        my_database.edit(my_model.User, 999999, {"description": "x"})


def test_edit_rejects_a_result_that_would_violate_the_model() -> None:
    created = my_database.add(_make_user())
    with pytest.raises(ValidationError):
        my_database.edit(my_model.User, created.id, {"username": None})


def test_delete_removes_the_record() -> None:
    created = my_database.add(_make_user())
    my_database.delete(my_model.User, created.id)
    with pytest.raises(my_database.errors.NotFoundError):
        my_database.read(my_model.User, created.id)


def test_delete_missing_identifier_raises_not_found() -> None:
    with pytest.raises(my_database.errors.NotFoundError):
        my_database.delete(my_model.User, 999999)


def test_status_enable_and_disable() -> None:
    created = my_database.add(_make_user())
    disabled = my_database.set_status(my_model.User, created.id, "disable")
    assert disabled.status is False
    enabled = my_database.set_status(my_model.User, created.id, "enable")
    assert enabled.status is True


def test_status_rejected_for_a_model_without_a_status_field() -> None:
    class StatuslessModel(my_model.BaseModel):
        id: int
        name: str

    with pytest.raises(my_database.errors.StatusNotSupportedError):
        my_database.set_status(StatuslessModel, 1, "enable")


def test_uniqueness_violation_is_rejected() -> None:
    my_database.add(_make_user(name="Admin"))
    with pytest.raises(my_database.errors.ConstraintViolationError):
        my_database.add(_make_user(name="Admin", username="different"))


def test_foreign_key_to_a_nonexistent_record_is_rejected() -> None:
    with pytest.raises(my_database.errors.ConstraintViolationError):
        my_database.add(my_model.Broker(id=0, name="FxPro", user_id=999999))


def test_credential_fields_are_never_exposed_in_a_read_result() -> None:
    created = my_database.add(_make_user())
    fetched = my_database.read(my_model.User, created.id)
    assert fetched.password == _credentials.REDACTED
    assert fetched.api_key == _credentials.REDACTED
