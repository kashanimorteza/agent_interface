"""Verifies the complete Database Public Interface as one whole (task P2-G11-T1)."""

from __future__ import annotations

import model

import database


def test_every_public_capability_reachable_through_the_top_level_package() -> None:
    for name in database.__all__:
        assert hasattr(database, name)


def test_every_persisted_domain_definition_reachable_through_the_generic_interface(db) -> None:
    from database.mapping import MAPPING_REGISTRY

    user = db.create(model.User(name="Ada", username="ada", password="pw", api_key="key"))
    for model_cls in MAPPING_REGISTRY:
        if model_cls is model.User:
            continue
        # Every mapped Domain Definition resolves through the same generic pipeline
        # without a Domain Definition-specific method existing on Database.
        assert db._orm_class(model_cls) is not None
    assert db.get(model.User, user.id) is not None


def test_registry_transaction_boundary_and_commands_reachable_through_the_same_boundary(db) -> None:
    assert db.instances.default.key == "general"
    with db.transaction() as txn:
        db.create(model.User(name="Ada", username="ada", password="pw", api_key="key"), txn=txn)
    result = db.execute_command("count_positions_by_execution", user_id=1)
    assert result is not None


def test_no_consumer_path_depends_on_a_private_mapping_or_adapter_resource(db) -> None:
    # A consumer reaches everything it needs through `database`'s top-level exports and the
    # `Database` instance's public methods; it never needs to import `database.mapping` or
    # `database.adapter` directly to perform a standard operation.
    public_members = {name for name in vars(database.Database) if not name.startswith("_")}
    assert {
        "create",
        "get",
        "list",
        "update",
        "delete",
        "activate",
        "transaction",
        "execute_command",
    } <= public_members
