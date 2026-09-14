import pytest
from pydantic import ValidationError

from model import Asset, Broker, Currency


def test_currency_accepts_valid_data():
    currency = Currency(user_id=1, code="USD", symbol="$", country="United States")
    assert currency.decimal_digits == 2


def test_currency_rejects_code_of_wrong_length():
    with pytest.raises(ValidationError):
        Currency(user_id=1, code="US")


def test_currency_declares_per_user_code_uniqueness_metadata():
    assert Currency.unique_together == (("user_id", "code"),)


def test_broker_accepts_valid_data():
    broker = Broker(name="FxPro", user_id=1)
    assert broker.is_active is True


def test_broker_declares_per_user_name_uniqueness_metadata():
    assert Broker.unique_together == (("user_id", "name"),)


def test_asset_accepts_valid_data():
    asset = Asset(
        broker_id=1, symbol="EUR/USD", category="Currency", point_size=0.0001, digits=5
    )
    assert asset.category == "Currency"


def test_asset_declares_per_broker_symbol_uniqueness_metadata():
    assert Asset.unique_together == (("broker_id", "symbol"),)
