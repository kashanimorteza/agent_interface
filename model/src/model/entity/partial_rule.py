"""The Partial Rule Domain Definition."""

from typing import Annotated

from model.entity.partial_group import PartialGroup
from model.foundation import (
    Constraint,
    Declare,
    ExactDecimal,
    ModelFoundation,
    Relationship,
)

__all__ = ["PartialRule"]


class PartialRule(
    ModelFoundation,
    description="Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.",
    persistent="persistent",
    relationships=(
        Relationship(
            name="partial_group",
            description="Belongs to one Partial Group through `partial_group_id`.",
            definition=PartialGroup,
            cardinality="1",
            optional=False,
        ),
    ),
    composite_constraints=(
        Constraint(
            id="partial_rule_partial_group_id_profit_percentage_unique",
            description="The combination of `partial_group_id` and `profit_percentage` must be unique.",
        ),
    ),
):
    id: Annotated[
        int,
        Declare(
            description="The unique identity of the partial rule.",
            logical_type="integer",
            identity=True,
            generated=True,
        ),
    ]
    name: Annotated[
        str,
        Declare(
            description="The partial rule's display name.",
            logical_type="string",
            unique=True,
        ),
    ]
    partial_group_id: Annotated[
        int,
        Declare(
            description="Identifies the partial group that contains the rule.",
            logical_type="integer",
        ),
    ]
    profit_percentage: Annotated[
        ExactDecimal,
        Declare(
            description="Defines the profit percentage that activates the rule.",
            logical_type="decimal",
        ),
    ]
    close_percentage: Annotated[
        ExactDecimal,
        Declare(
            description="Defines the percentage of the position closed when the rule is activated.",
            logical_type="decimal",
        ),
    ]
    is_active: Annotated[
        bool,
        Declare(
            description="Indicates whether the partial rule is active.",
            logical_type="boolean",
        ),
    ] = True
    description: Annotated[
        str | None,
        Declare(description="Describes the partial rule.", logical_type="string"),
    ]
