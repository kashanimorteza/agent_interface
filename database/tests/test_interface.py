"""Verifies the generic, Model-driven Database Interface."""

from __future__ import annotations

import pytest
from model import Broker, User
from sqlalchemy.exc import IntegrityError

from database import (
    ActivationNotSupportedError,
    RecordNotFoundError,
    UnknownSearchFieldError,
)
from database.credentials import verify_hash
from database.interface import DatabaseInterface, UnknownControlledCommandError


def _user(name: str, username: str) -> User:
    return User(id=0, name=name, username=username, password="s3cret", api_key="k3y")


def test_create_assigns_autoincrement_id_ignoring_caller_placeholder(
    db: DatabaseInterface,
) -> None:
    first = db.create(_user("A", "a"))
    second = db.create(_user("B", "b"))
    assert first.id != second.id
    assert first.id is not None
    assert second.id is not None


def test_create_applies_declared_credential_treatment(db: DatabaseInterface) -> None:
    created = db.create(_user("Admin", "admin"))
    assert created.password != "s3cret"
    assert verify_hash("s3cret", created.password)


def test_get_by_id_returns_none_when_missing(db: DatabaseInterface) -> None:
    assert db.get_by_id(User, 999) is None


def test_get_by_id_returns_the_created_record(db: DatabaseInterface) -> None:
    created = db.create(_user("Admin", "admin"))
    fetched = db.get_by_id(User, created.id)
    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.name == "Admin"


def test_list_returns_every_record(db: DatabaseInterface) -> None:
    db.create(_user("A", "a"))
    db.create(_user("B", "b"))
    assert len(db.list(User)) == 2


def test_search_filters_by_criteria(db: DatabaseInterface) -> None:
    db.create(_user("A", "a"))
    db.create(_user("B", "b"))
    result = db.search(User, {"username": "b"})
    assert len(result) == 1
    assert result[0].username == "b"


def test_search_rejects_unknown_field(db: DatabaseInterface) -> None:
    with pytest.raises(UnknownSearchFieldError):
        db.search(User, {"not_a_field": 1})


def test_update_changes_only_named_fields(db: DatabaseInterface) -> None:
    created = db.create(_user("Admin", "admin"))
    updated = db.update(User, created.id, {"description": "changed"})
    assert updated.description == "changed"
    assert updated.username == "admin"


def test_update_applies_credential_treatment_to_changed_credential(
    db: DatabaseInterface,
) -> None:
    created = db.create(_user("Admin", "admin"))
    updated = db.update(User, created.id, {"password": "new-secret"})
    assert updated.password != "new-secret"
    assert verify_hash("new-secret", updated.password)


def test_update_missing_record_raises(db: DatabaseInterface) -> None:
    with pytest.raises(RecordNotFoundError):
        db.update(User, 999, {"description": "x"})


def test_delete_removes_the_record(db: DatabaseInterface) -> None:
    created = db.create(_user("Admin", "admin"))
    db.delete(User, created.id)
    assert db.get_by_id(User, created.id) is None


def test_delete_missing_record_raises(db: DatabaseInterface) -> None:
    with pytest.raises(RecordNotFoundError):
        db.delete(User, 999)


def test_enable_disable_flip_is_active(db: DatabaseInterface) -> None:
    created = db.create(_user("Admin", "admin"))
    disabled = db.disable(User, created.id)
    assert disabled.is_active is False
    enabled = db.enable(User, created.id)
    assert enabled.is_active is True


def test_activation_rejected_when_domain_definition_has_no_is_active(
    db: DatabaseInterface, monkeypatch: pytest.MonkeyPatch
) -> None:
    from sqlalchemy import Column, Integer, MetaData, String, Table

    import database.interface as interface_module

    fake_metadata = MetaData()
    fake_table = Table(
        "no_active_things",
        fake_metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String),
    )

    def _fake_table_for(_adapter: object, _model_cls: object) -> Table:
        return fake_table

    monkeypatch.setattr(interface_module, "_table_for", _fake_table_for)
    with pytest.raises(ActivationNotSupportedError):
        db.set_active(User, 1, True)


def test_referenced_record_existence_is_enforced(db: DatabaseInterface) -> None:
    with pytest.raises(IntegrityError):
        db.create(Broker(id=0, name="FxPro", user_id=999999))


def test_transaction_commits_grouped_operations_together(db: DatabaseInterface) -> None:
    with db.transaction() as txn:
        db.create(_user("A", "a"), txn=txn)
        db.create(_user("B", "b"), txn=txn)
    assert len(db.list(User)) == 2


def test_transaction_rolls_back_every_operation_on_failure(
    db: DatabaseInterface,
) -> None:
    with pytest.raises(IntegrityError), db.transaction() as txn:
        db.create(_user("A", "a"), txn=txn)
        db.create(_user("A", "dup-name"), txn=txn)  # violates unique name
    assert len(db.list(User)) == 0


def test_standalone_write_is_unaffected_by_a_later_failed_transaction(
    db: DatabaseInterface,
) -> None:
    standalone = db.create(_user("Standalone", "standalone"))
    with pytest.raises(IntegrityError), db.transaction() as txn:
        db.create(_user("Standalone", "dup"), txn=txn)  # violates unique name
    assert db.get_by_id(User, standalone.id) is not None


def test_controlled_command_count(db: DatabaseInterface) -> None:
    db.create(_user("A", "a"))
    db.create(_user("B", "b"))
    db.disable(User, db.search(User, {"username": "b"})[0].id)
    active_count = db.execute_command(
        "count", model_cls=User, criteria={"is_active": True}
    )
    assert active_count == 1


def test_controlled_command_rejects_unknown_name(db: DatabaseInterface) -> None:
    with pytest.raises(UnknownControlledCommandError):
        db.execute_command("drop_table", model_cls=User)


def test_controlled_command_route_has_no_structural_or_migration_command_allow_listed() -> (
    None
):
    from database.interface import _ALLOWED_CONTROLLED_COMMANDS

    forbidden = {
        "drop_table",
        "alter_table",
        "create_table",
        "grant",
        "revoke",
        "migrate",
        "upgrade",
        "downgrade",
    }
    assert _ALLOWED_CONTROLLED_COMMANDS.isdisjoint(forbidden)
