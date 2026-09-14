from __future__ import annotations

import model
import pytest

from database import DatabaseInterface, NotFoundError
from database.interface import PROTECTED_VALUE_PLACEHOLDER

ALL_DOMAIN_DEFINITIONS = [
    model.User,
    model.TradingPlatform,
    model.Broker,
    model.Instance,
    model.Currency,
    model.Asset,
    model.AccountGroup,
    model.Account,
    model.TrailingGroup,
    model.TrailingRule,
    model.PartialGroup,
    model.PartialRule,
    model.ActionGroup,
    model.Action,
    model.Position,
]


@pytest.mark.parametrize("model_cls", ALL_DOMAIN_DEFINITIONS)
def test_create_assigns_a_real_persisted_id(
    db: DatabaseInterface,
    graph: dict[type[model.ModelFoundation], model.ModelFoundation],
    model_cls: type[model.ModelFoundation],
) -> None:
    created = graph[model_cls]
    assert isinstance(created.id, int)


@pytest.mark.parametrize("model_cls", ALL_DOMAIN_DEFINITIONS)
def test_get_by_id_round_trips_non_credential_fields(
    db: DatabaseInterface,
    graph: dict[type[model.ModelFoundation], model.ModelFoundation],
    model_cls: type[model.ModelFoundation],
) -> None:
    created = graph[model_cls]
    fetched = db.get_by_id(model_cls, created.id)
    assert fetched is not None
    credential_fields = model_cls.credential_storage()
    for field in model_cls.model_fields:
        if field in credential_fields:
            continue
        assert getattr(fetched, field) == getattr(created, field), field


@pytest.mark.parametrize("model_cls", ALL_DOMAIN_DEFINITIONS)
def test_get_by_id_masks_credential_fields(
    db: DatabaseInterface,
    graph: dict[type[model.ModelFoundation], model.ModelFoundation],
    model_cls: type[model.ModelFoundation],
) -> None:
    created = graph[model_cls]
    credential_fields = model_cls.credential_storage()
    if not credential_fields:
        pytest.skip(f"{model_cls.__name__} declares no credential Fields")
    fetched = db.get_by_id(model_cls, created.id)
    assert fetched is not None
    for field in credential_fields:
        assert getattr(fetched, field) == PROTECTED_VALUE_PLACEHOLDER
        assert getattr(fetched, field) != getattr(created, field)


@pytest.mark.parametrize("model_cls", ALL_DOMAIN_DEFINITIONS)
def test_get_by_id_returns_none_for_unknown_id(
    db: DatabaseInterface, model_cls: type[model.ModelFoundation]
) -> None:
    assert db.get_by_id(model_cls, 999_999) is None


@pytest.mark.parametrize("model_cls", ALL_DOMAIN_DEFINITIONS)
def test_list_includes_created_record(
    db: DatabaseInterface,
    graph: dict[type[model.ModelFoundation], model.ModelFoundation],
    model_cls: type[model.ModelFoundation],
) -> None:
    created = graph[model_cls]
    listed_ids = {record.id for record in db.list(model_cls)}
    assert created.id in listed_ids


@pytest.mark.parametrize("model_cls", ALL_DOMAIN_DEFINITIONS)
def test_search_filters_by_criteria(
    db: DatabaseInterface,
    graph: dict[type[model.ModelFoundation], model.ModelFoundation],
    model_cls: type[model.ModelFoundation],
) -> None:
    created = graph[model_cls]
    found = db.search(model_cls, id=created.id)
    assert [r.id for r in found] == [created.id]
    not_found = db.search(model_cls, id=999_999)
    assert not_found == []


@pytest.mark.parametrize("model_cls", ALL_DOMAIN_DEFINITIONS)
def test_enable_and_disable_change_only_is_active(
    db: DatabaseInterface,
    graph: dict[type[model.ModelFoundation], model.ModelFoundation],
    model_cls: type[model.ModelFoundation],
) -> None:
    created = graph[model_cls]
    disabled = db.disable(model_cls, created.id)
    assert disabled.is_active is False
    for field in model_cls.model_fields:
        if field in ("is_active", *model_cls.credential_storage()):
            continue
        assert getattr(disabled, field) == getattr(created, field), field

    enabled = db.enable(model_cls, created.id)
    assert enabled.is_active is True


@pytest.mark.parametrize("model_cls", ALL_DOMAIN_DEFINITIONS)
def test_delete_removes_the_record(
    db: DatabaseInterface,
    graph: dict[type[model.ModelFoundation], model.ModelFoundation],
    model_cls: type[model.ModelFoundation],
) -> None:
    # Position has no dependents in this Plan, so it is the only Domain Definition
    # deletable without first removing everything that references it; every other
    # mapped type in `graph` has at least one dependent record, so RESTRICT correctly
    # rejects deleting it (proven separately in test_referential_integrity.py).
    if model_cls is not model.Position:
        pytest.skip("covered by test_referential_integrity.py's RESTRICT proof instead")
    created = graph[model_cls]
    db.delete(model_cls, created.id)
    assert db.get_by_id(model_cls, created.id) is None


def test_delete_unknown_id_raises_not_found(db: DatabaseInterface) -> None:
    with pytest.raises(NotFoundError):
        db.delete(model.User, 999_999)


def test_update_changes_a_field_and_round_trips_the_rest(
    db: DatabaseInterface, graph: dict[type[model.ModelFoundation], model.ModelFoundation]
) -> None:
    user = graph[model.User]
    changed = user.model_copy(update={"description": "updated via test"})
    result = db.update(changed)
    assert result.description == "updated via test"
    fetched = db.get_by_id(model.User, user.id)
    assert fetched is not None
    assert fetched.description == "updated via test"
    assert fetched.name == user.name


def test_update_unknown_id_raises_not_found(db: DatabaseInterface) -> None:
    ghost = model.User(id=999_999, name="Ghost", username="ghost", password="p", api_key="k")
    with pytest.raises(NotFoundError):
        db.update(ghost)
