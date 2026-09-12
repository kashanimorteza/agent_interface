"""Initial data seeding: dependency order, generated fields, repeatability."""

import my_model

import my_database


def test_seeding_inserts_every_declared_initial_record() -> None:
    result = my_database.seed_initial_data()
    assert result == {
        "User": 1,
        "TradingPlatform": 2,
        "Instance": 1,
        "Currency": 8,
        "Broker": 1,
        "Asset": 4,
        "AccountGroup": 1,
        "Account": 1,
        "TrailingGroup": 1,
        "PartialGroup": 1,
        "ActionGroup": 1,
        "Action": 1,
    }


def test_seeded_relationships_resolve_correctly() -> None:
    my_database.seed_initial_data()
    instance = my_database.list_records(my_model.Instance)[0]
    platform = my_database.read(my_model.TradingPlatform, instance.trading_platform_id)
    assert platform.code == "metatrader_5"


def test_seeded_credential_fields_are_generated_and_protected() -> None:
    my_database.seed_initial_data()
    user = my_database.list_records(my_model.User)[0]
    assert user.password == "<redacted>"
    instance = my_database.list_records(my_model.Instance)[0]
    assert instance.password  # decrypted, non-empty generated value


def test_seeding_twice_does_not_duplicate_records() -> None:
    my_database.seed_initial_data()
    second = my_database.seed_initial_data()
    assert all(count == 0 for count in second.values())
    assert len(my_database.list_records(my_model.User)) == 1
    assert len(my_database.list_records(my_model.Currency, limit=20)) == 8
