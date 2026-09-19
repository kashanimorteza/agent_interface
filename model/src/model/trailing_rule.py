"""Trailing Rule: when and how a Trailing Group manages Take Profit and Stop Loss."""

from typing import Annotated

from .foundation import ExactDecimal, Flag, GeneratedId, Integer, ModelFoundation, Relationship, Text, Unique
from .trailing_group import TrailingGroup


class TrailingRule(ModelFoundation):
    persistence = "persistent"
    relationships = (
        Relationship(field="trailing_group_id", reference=TrailingGroup, reference_field="id", cardinality="many-to-one", optional=False),
    )
    unique_sets = (("trailing_group_id", "trigger_percentage"),)

    id: GeneratedId = None
    name: Annotated[Text, Unique()]
    trailing_group_id: Integer
    trigger_percentage: ExactDecimal
    take_profit_adjustment: ExactDecimal | None = None
    stop_loss_adjustment: ExactDecimal | None = None
    is_active: Flag = True
    description: Text | None = None
