from decimal import Decimal

from .foundation import ModelBase


class TrailingGroup(ModelBase):
    unique_together = (("user_id", "name"),)

    id: int | None = None
    user_id: int
    name: str
    is_active: bool = True
    description: str | None = None


class TrailingRule(ModelBase):
    unique_together = (("name",), ("trailing_group_id", "trigger_percentage"))

    id: int | None = None
    name: str
    trailing_group_id: int
    trigger_percentage: Decimal
    take_profit_adjustment: Decimal | None = None
    stop_loss_adjustment: Decimal | None = None
    is_active: bool = True
    description: str | None = None


class PartialGroup(ModelBase):
    unique_together = (("user_id", "name"),)

    id: int | None = None
    user_id: int
    name: str
    is_active: bool = True
    description: str | None = None


class PartialRule(ModelBase):
    unique_together = (("name",), ("partial_group_id", "profit_percentage"))

    id: int | None = None
    name: str
    partial_group_id: int
    profit_percentage: Decimal
    close_percentage: Decimal
    is_active: bool = True
    description: str | None = None
