from __future__ import annotations

from decimal import Decimal
from typing import ClassVar

from pydantic import Field

from ._base import DomainModel
from ._shared import Relationship


class TrailingRule(DomainModel):
    name: str = Field(..., description="The trailing rule's display name.")
    trailing_group_id: int = Field(
        ..., description="Identifies the trailing group that contains the rule."
    )
    trigger_percentage: Decimal = Field(
        ..., description="Defines the profit percentage of the take-profit target that activates the rule."
    )
    take_profit_adjustment: Decimal | None = Field(
        default=None, description="Defines the take-profit adjustment applied when the rule is activated."
    )
    stop_loss_adjustment: Decimal | None = Field(
        default=None, description="Defines the stop-loss adjustment applied when the rule is activated."
    )
    status: bool = Field(default=True, description="Indicates whether the trailing rule is active.")
    description: str | None = Field(default=None, description="Describes the trailing rule.")

    unique_fields: ClassVar[frozenset[str]] = frozenset({"name"})
    unique_together: ClassVar[list[tuple[str, ...]]] = [("trailing_group_id", "trigger_percentage")]
    relationships: ClassVar[dict[str, Relationship]] = {
        "trailing_group": Relationship(
            target="TrailingGroup", cardinality="one", field="trailing_group_id"
        ),
    }
