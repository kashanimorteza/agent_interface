"""The Action Group Domain Definition."""

from typing import Annotated

from model.entity.user import User
from model.foundation import (
    Constraint,
    Declare,
    ModelFoundation,
    Relationship,
)

__all__ = ["ActionGroup"]


class ActionGroup(
    ModelFoundation,
    description="Defines an independent grouping for trading actions based on their risk profile, such as high risk, normal risk, or low risk. Actions are assigned to these groups so trades can be organized and selected by their intended risk level.",
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
            id="action_group_user_id_name_unique",
            description="The combination of `user_id` and `name` must be unique.",
        ),
    ),
):
    id: Annotated[
        int,
        Declare(
            description="The unique identity of the action group.",
            logical_type="integer",
            identity=True,
            generated=True,
        ),
    ]
    user_id: Annotated[
        int,
        Declare(
            description="Identifies the user who owns the action group.",
            logical_type="integer",
        ),
    ]
    name: Annotated[
        str,
        Declare(description="The action group's display name.", logical_type="string"),
    ]
    is_active: Annotated[
        bool,
        Declare(
            description="Indicates whether the action group is active.",
            logical_type="boolean",
        ),
    ] = True
    description: Annotated[
        str | None,
        Declare(description="Describes the action group.", logical_type="string"),
    ]
