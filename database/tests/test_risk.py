from decimal import Decimal

import pytest
from model import PartialGroup, PartialRule, TrailingGroup, TrailingRule, User
from pydantic import SecretStr
from sqlalchemy.exc import IntegrityError

from database import create, transaction


def _make_user(tx) -> int:
    user = create(
        User(name="U", username="u", password=SecretStr("p"), api_key=SecretStr("k")),
        session=tx,
    )
    assert user.id is not None
    return user.id


def test_trailing_rule_persists_and_enforces_per_group_trigger_uniqueness():
    with transaction() as tx:
        user_id = _make_user(tx)
        group = create(TrailingGroup(user_id=user_id, name="Default"), session=tx)
        assert group.id is not None
        create(
            TrailingRule(
                name="TR-1", trailing_group_id=group.id, trigger_percentage=Decimal(50)
            ),
            session=tx,
        )
        group_id = group.id

    with pytest.raises(IntegrityError), transaction() as tx:
        create(
            TrailingRule(
                name="TR-2", trailing_group_id=group_id, trigger_percentage=Decimal(50)
            ),
            session=tx,
        )


def test_partial_rule_persists_and_enforces_per_group_profit_uniqueness():
    with transaction() as tx:
        user_id = _make_user(tx)
        group = create(PartialGroup(user_id=user_id, name="Default"), session=tx)
        assert group.id is not None
        create(
            PartialRule(
                name="PR-1",
                partial_group_id=group.id,
                profit_percentage=Decimal(50),
                close_percentage=Decimal(50),
            ),
            session=tx,
        )
        group_id = group.id

    with pytest.raises(IntegrityError), transaction() as tx:
        create(
            PartialRule(
                name="PR-2",
                partial_group_id=group_id,
                profit_percentage=Decimal(50),
                close_percentage=Decimal(25),
            ),
            session=tx,
        )
