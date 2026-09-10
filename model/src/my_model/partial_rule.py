from __future__ import annotations

from decimal import Decimal
from typing import ClassVar

from pydantic import Field

from ._base import DomainModel
from ._shared import Relationship


class PartialRule(DomainModel):
    name: str = Field(..., description="The partial rule's display name.")
    partial_group_id: int = Field(..., description="Identifies the partial group that contains the rule.")
    profit_percentage: Decimal = Field(
        ..., description="Defines the profit percentage that activates the rule."
    )
    close_percentage: Decimal = Field(
        ..., description="Defines the percentage of the position closed when the rule is activated."
    )
    status: bool = Field(default=True, description="Indicates whether the partial rule is active.")
    description: str | None = Field(default=None, description="Describes the partial rule.")

    unique_fields: ClassVar[frozenset[str]] = frozenset({"name"})
    unique_together: ClassVar[list[tuple[str, ...]]] = [("partial_group_id", "profit_percentage")]
    relationships: ClassVar[dict[str, Relationship]] = {
        "partial_group": Relationship(target="PartialGroup", cardinality="one", field="partial_group_id"),
    }
