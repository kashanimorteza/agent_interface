"""The Trailing Rule Domain Definition."""

from typing import Annotated

from model.entity.trailing_group import TrailingGroup
from model.foundation import (
    Constraint,
    Declare,
    ExactDecimal,
    ModelFoundation,
    Relationship,
)

__all__ = ["TrailingRule"]


class TrailingRule(
    ModelFoundation,
    description="Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.",
    persistent="persistent",
    relationships=(
        Relationship(
            name="trailing_group",
            description="Belongs to one Trailing Group through `trailing_group_id`.",
            definition=TrailingGroup,
            cardinality="1",
            optional=False,
        ),
    ),
    composite_constraints=(
        Constraint(
            id="trailing_rule_trailing_group_id_trigger_percentage_unique",
            description="The combination of `trailing_group_id` and `trigger_percentage` must be unique.",
        ),
    ),
):
    id: Annotated[
        int,
        Declare(
            description="The unique identity of the trailing rule.",
            logical_type="integer",
            identity=True,
            generated=True,
        ),
    ]
    name: Annotated[
        str,
        Declare(
            description="The trailing rule's display name.",
            logical_type="string",
            unique=True,
        ),
    ]
    trailing_group_id: Annotated[
        int,
        Declare(
            description="Identifies the trailing group that contains the rule.",
            logical_type="integer",
        ),
    ]
    trigger_percentage: Annotated[
        ExactDecimal,
        Declare(
            description="Defines the profit percentage of the take-profit target that activates the rule.",
            logical_type="decimal",
        ),
    ]
    take_profit_adjustment: Annotated[
        ExactDecimal | None,
        Declare(
            description="Defines the take-profit adjustment applied when the rule is activated.",
            logical_type="decimal",
        ),
    ]
    stop_loss_adjustment: Annotated[
        ExactDecimal | None,
        Declare(
            description="Defines the stop-loss adjustment applied when the rule is activated.",
            logical_type="decimal",
        ),
    ]
    is_active: Annotated[
        bool,
        Declare(
            description="Indicates whether the trailing rule is active.",
            logical_type="boolean",
        ),
    ] = True
    description: Annotated[
        str | None,
        Declare(description="Describes the trailing rule.", logical_type="string"),
    ]
