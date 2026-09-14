from pydantic import SecretStr

from model import Account, AccountGroup


def test_account_group_accepts_valid_data():
    group = AccountGroup(user_id=1, name="Default")
    assert group.is_active is True


def test_account_group_declares_per_user_name_uniqueness_metadata():
    assert AccountGroup.unique_together == (("user_id", "name"),)


def test_account_accepts_valid_data_and_protects_password():
    account = Account(
        name="Acc-1",
        group_id=1,
        broker_id=1,
        instance_id=1,
        base_currency_id=1,
        username="test",
        password=SecretStr("secret"),
        leverage=100,
        account_type="CFD",
    )
    assert "secret" not in str(account)
    assert account.balance == 0
    assert account.password.get_secret_value() == "secret"


def test_account_declares_name_and_group_broker_instance_uniqueness_metadata():
    assert Account.unique_together == (
        ("name",),
        ("group_id", "broker_id", "instance_id"),
    )
