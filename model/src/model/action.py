"""Action Domain Definition.

Represents how a position must be opened: selects the Asset traded and
the Account used, and the risk, Take Profit, Stop Loss, Partial Group, and
Trailing Group settings that determine the position's parameters and
execution behavior.
"""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from model.foundation import DomainModel


class Action(DomainModel):
    """A trading action definition used to open a Position."""

    persistent = True
    unique_sets = (("action_group_id", "name"),)

    id: int | None = Field(
        default=None,
        json_schema_extra={
            "type": "integer",
            "primary_key": True,
            "auto_increment": True,
            "nullable": False,
        },
    )
    name: str = Field(
        json_schema_extra={"type": "string", "nullable": False},
    )
    action_group_id: int = Field(
        json_schema_extra={
            "type": "integer",
            "nullable": False,
            "foreign_key": {"references": "ActionGroup", "field": "id"},
            "cardinality": {
                "of": "Action",
                "to": "ActionGroup",
                "multiplicity": "many-to-one",
                "optional": False,
            },
        },
    )
    asset_id: int = Field(
        json_schema_extra={
            "type": "integer",
            "nullable": False,
            "foreign_key": {"references": "Asset", "field": "id"},
            "cardinality": {
                "of": "Action",
                "to": "Asset",
                "multiplicity": "many-to-one",
                "optional": False,
            },
        },
    )
    account_id: int = Field(
        json_schema_extra={
            "type": "integer",
            "nullable": False,
            "foreign_key": {"references": "Account", "field": "id"},
            "cardinality": {
                "of": "Action",
                "to": "Account",
                "multiplicity": "many-to-one",
                "optional": False,
            },
        },
    )
    partial_group_id: int = Field(
        json_schema_extra={
            "type": "integer",
            "nullable": False,
            "foreign_key": {"references": "PartialGroup", "field": "id"},
            "cardinality": {
                "of": "Action",
                "to": "PartialGroup",
                "multiplicity": "many-to-one",
                "optional": False,
            },
        },
    )
    trailing_group_id: int = Field(
        json_schema_extra={
            "type": "integer",
            "nullable": False,
            "foreign_key": {"references": "TrailingGroup", "field": "id"},
            "cardinality": {
                "of": "Action",
                "to": "TrailingGroup",
                "multiplicity": "many-to-one",
                "optional": False,
            },
        },
    )
    risk_by_reward: Decimal = Field(
        json_schema_extra={"type": "decimal", "nullable": False},
    )
    take_profit: Decimal = Field(
        json_schema_extra={"type": "decimal", "nullable": False},
    )
    stop_loss: Decimal = Field(
        json_schema_extra={"type": "decimal", "nullable": False},
    )
    is_active: bool = Field(
        default=True,
        json_schema_extra={"type": "boolean", "nullable": False, "default": True},
    )
    description: str | None = Field(
        default=None,
        json_schema_extra={"type": "string", "nullable": True},
    )
