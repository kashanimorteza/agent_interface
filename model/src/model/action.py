"""Action Domain Definition."""

from __future__ import annotations

from decimal import Decimal
from typing import Annotated

from pydantic import Field

from model.foundation import DomainModel, FieldMeta, ForeignKey, PersistenceMeta


class Action(DomainModel):
    """Defines how a position must be opened: asset, account, risk, and rule-group selections."""

    id: Annotated[int | None, FieldMeta(primary_key=True, auto_increment=True, nullable=False)] = (
        None
    )
    name: Annotated[str, FieldMeta(nullable=False)] = Field(min_length=1)
    action_group_id: Annotated[
        int, FieldMeta(nullable=False, foreign_key=ForeignKey("ActionGroup", "id"))
    ]
    asset_id: Annotated[int, FieldMeta(nullable=False, foreign_key=ForeignKey("Asset", "id"))]
    account_id: Annotated[int, FieldMeta(nullable=False, foreign_key=ForeignKey("Account", "id"))]
    partial_group_id: Annotated[
        int, FieldMeta(nullable=False, foreign_key=ForeignKey("PartialGroup", "id"))
    ]
    trailing_group_id: Annotated[
        int, FieldMeta(nullable=False, foreign_key=ForeignKey("TrailingGroup", "id"))
    ]
    risk_by_reward: Annotated[Decimal, FieldMeta(nullable=False)]
    take_profit: Annotated[Decimal, FieldMeta(nullable=False)]
    stop_loss: Annotated[Decimal, FieldMeta(nullable=False)]
    is_active: Annotated[bool, FieldMeta(nullable=False, default=True)] = True
    description: Annotated[str | None, FieldMeta(nullable=True)] = None

    class Meta(PersistenceMeta):
        persistent = True
        unique_sets = (("action_group_id", "name"),)
