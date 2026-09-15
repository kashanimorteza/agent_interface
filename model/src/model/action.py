"""The Action Domain Definition."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from model.foundation import DomainModel, field_meta


class Action(DomainModel):
    """How a position must be opened: asset, account, risk, and rule-group selections."""

    __persistent__ = True
    __unique_sets__ = (("action_group_id", "name"),)

    id: int = Field(json_schema_extra=field_meta(primary_key=True, auto_increment=True))
    name: str = Field(json_schema_extra=field_meta())
    action_group_id: int = Field(
        json_schema_extra=field_meta(
            foreign_key="action_group.id", cardinality="many_to_one"
        )
    )
    asset_id: int = Field(
        json_schema_extra=field_meta(foreign_key="asset.id", cardinality="many_to_one")
    )
    account_id: int = Field(
        json_schema_extra=field_meta(
            foreign_key="account.id", cardinality="many_to_one"
        )
    )
    partial_group_id: int = Field(
        json_schema_extra=field_meta(
            foreign_key="partial_group.id", cardinality="many_to_one"
        )
    )
    trailing_group_id: int = Field(
        json_schema_extra=field_meta(
            foreign_key="trailing_group.id", cardinality="many_to_one"
        )
    )
    risk_by_reward: Decimal = Field(json_schema_extra=field_meta())
    take_profit: Decimal = Field(json_schema_extra=field_meta())
    stop_loss: Decimal = Field(json_schema_extra=field_meta())
    is_active: bool = Field(default=True, json_schema_extra=field_meta())
    description: str | None = Field(
        default=None, json_schema_extra=field_meta(nullable=True)
    )
