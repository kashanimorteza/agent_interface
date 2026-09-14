from model import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    Currency,
    Instance,
    PartialGroup,
    Position,
    TradingPlatform,
    TrailingGroup,
    User,
)

from database import list_, seed_initial_data, transaction


def test_seeding_twice_creates_no_duplicate_record():
    first = seed_initial_data()
    assert "User.Admin.password" in first
    assert "Instance.MetaTrader.password" in first
    assert "Account.Acc-1.password" in first

    second = seed_initial_data()
    assert second == {}

    with transaction() as tx:
        assert len(list_(User, session=tx)) == 1
        assert len(list_(TradingPlatform, session=tx)) == 2
        assert len(list_(Currency, session=tx)) == 8
        assert len(list_(Broker, session=tx)) == 1
        assert len(list_(Instance, session=tx)) == 1
        assert len(list_(Asset, session=tx)) == 4
        assert len(list_(AccountGroup, session=tx)) == 1
        assert len(list_(TrailingGroup, session=tx)) == 1
        assert len(list_(PartialGroup, session=tx)) == 1
        assert len(list_(ActionGroup, session=tx)) == 1
        assert len(list_(Account, session=tx)) == 1
        assert len(list_(Action, session=tx)) == 1
        assert len(list_(Position, session=tx)) == 0
