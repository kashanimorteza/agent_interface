import pytest
from model import Currency, TradingPlatform, User
from pydantic import SecretStr
from sqlalchemy.exc import IntegrityError

from database import create, delete, get_by_id, list_, set_active, transaction, update


def _generic_lifecycle(model_type, build):
    with transaction() as tx:
        created = create(build(), session=tx)
        assert created.id is not None

        fetched = get_by_id(model_type, created.id, session=tx)
        assert fetched is not None
        assert fetched.id == created.id

        listed = list_(model_type, session=tx)
        assert any(row.id == created.id for row in listed)

        disabled = set_active(model_type, created.id, False, session=tx)
        assert disabled.is_active is False
        enabled = set_active(model_type, created.id, True, session=tx)
        assert enabled.is_active is True

        delete(model_type, created.id, session=tx)
        assert get_by_id(model_type, created.id, session=tx) is None


def test_generic_operations_work_identically_for_two_unrelated_models():
    _generic_lifecycle(
        TradingPlatform,
        lambda: TradingPlatform(name="MetaTrader 5", code="metatrader_5"),
    )

    with transaction() as tx:
        user = create(
            User(
                name="U", username="u", password=SecretStr("p"), api_key=SecretStr("k")
            ),
            session=tx,
        )
        assert user.id is not None
        user_id = user.id

    _generic_lifecycle(Currency, lambda: Currency(user_id=user_id, code="USD"))


def test_update_changes_fields_and_protects_a_changed_credential():
    with transaction() as tx:
        platform = create(
            TradingPlatform(name="MetaTrader 5", code="metatrader_5"), session=tx
        )
        assert platform.id is not None
        updated = update(
            TradingPlatform, platform.id, {"name": "MetaTrader 5 Renamed"}, session=tx
        )
        assert updated.name == "MetaTrader 5 Renamed"


def test_failed_operation_inside_a_transaction_leaves_no_partial_change():
    with transaction() as tx:
        user = create(
            User(
                name="V", username="v", password=SecretStr("p"), api_key=SecretStr("k")
            ),
            session=tx,
        )
        assert user.id is not None
        user_id = user.id

    with pytest.raises(IntegrityError), transaction() as tx:
        create(TradingPlatform(name="Keep-Out", code="keep-out"), session=tx)
        create(Currency(user_id=user_id, code="USD"), session=tx)
        create(Currency(user_id=user_id, code="USD"), session=tx)

    with transaction() as tx:
        assert list_(TradingPlatform, session=tx, code="keep-out") == []
        assert list_(Currency, session=tx, user_id=user_id, code="USD") == []
