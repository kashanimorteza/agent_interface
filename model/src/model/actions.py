from decimal import Decimal

from pydantic import AwareDatetime

from .foundation import ModelBase


class ActionGroup(ModelBase):
    unique_together = (("user_id", "name"),)

    id: int | None = None
    user_id: int
    name: str
    is_active: bool = True
    description: str | None = None


class Action(ModelBase):
    unique_together = (("action_group_id", "name"),)

    id: int | None = None
    name: str
    action_group_id: int
    asset_id: int
    account_id: int
    partial_group_id: int
    trailing_group_id: int
    risk_by_reward: Decimal
    take_profit: Decimal
    stop_loss: Decimal
    is_active: bool = True
    description: str | None = None


class Position(ModelBase):
    unique_together = (("name",),)

    id: int | None = None
    user_id: int
    name: str
    trading_platform_id: int
    broker_id: int
    account_id: int
    trailing_group_id: int
    partial_group_id: int
    action_group_id: int
    action_id: int
    date: AwareDatetime
    volume: Decimal
    profit: Decimal = Decimal(0)
    is_executed: bool = False
    order_type: str
    base_tp: Decimal
    base_sl: Decimal
    real_tp: Decimal
    real_sl: Decimal
    is_active: bool = True
    description: str | None = None
