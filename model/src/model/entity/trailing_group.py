"""The Trailing Group Domain Definition."""

from typing import Annotated

from model.entity.user import User
from model.foundation import (
    Constraint,
    Declare,
    ModelFoundation,
    Relationship,
)

__all__ = ["TrailingGroup"]


class TrailingGroup(
    ModelFoundation,
    description="Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply.",
    persistent="persistent",
    relationships=(
        Relationship(
            name="user",
            description="Belongs to one User through `user_id`.",
            definition=User,
            cardinality="1",
            optional=False,
        ),
    ),
    composite_constraints=(
        Constraint(
            id="trailing_group_user_id_name_unique",
            description="The combination of `user_id` and `name` must be unique.",
        ),
    ),
):
    id: Annotated[
        int,
        Declare(
            description="The unique identity of the trailing group.",
            logical_type="integer",
            identity=True,
            generated=True,
        ),
    ]
    user_id: Annotated[
        int,
        Declare(
            description="Identifies the user who owns the trailing group.",
            logical_type="integer",
        ),
    ]
    name: Annotated[
        str,
        Declare(
            description="The trailing group's display name.", logical_type="string"
        ),
    ]
    is_active: Annotated[
        bool,
        Declare(
            description="Indicates whether the trailing group is active.",
            logical_type="boolean",
        ),
    ] = True
    description: Annotated[
        str | None,
        Declare(description="Describes the trailing group.", logical_type="string"),
    ]
