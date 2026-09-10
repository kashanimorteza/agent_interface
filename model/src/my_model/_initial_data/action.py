from decimal import Decimal

from my_model._models.action import Action

RECORDS: tuple[Action, ...] = (
    Action(
        name="Default",
        action_group_id=1,
        asset_id=1,
        account_id=1,
        partial_group_id=1,
        trailing_group_id=1,
        risk_by_reward=Decimal("1"),
        take_profit=Decimal("1"),
        stop_loss=Decimal("1"),
    ),
)
