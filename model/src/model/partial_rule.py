"""Partial Rule: the condition and the share of volume a Partial Group closes."""

from typing import Annotated

from .foundation import ExactDecimal, Flag, GeneratedId, Integer, ModelFoundation, Relationship, Text, Unique
from .partial_group import PartialGroup


class PartialRule(ModelFoundation):
    persistence = "persistent"
    relationships = (Relationship(field="partial_group_id", reference=PartialGroup, reference_field="id", cardinality="many-to-one", optional=False),)
    unique_sets = (("partial_group_id", "profit_percentage"),)

    id: GeneratedId = None
    name: Annotated[Text, Unique()]
    partial_group_id: Integer
    profit_percentage: ExactDecimal
    close_percentage: ExactDecimal
    is_active: Flag = True
    description: Text | None = None
