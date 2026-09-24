"""The Partial Group Domain Definition."""

from typing import Annotated

from model.entity.user import User
from model.foundation import (
    Constraint,
    Declare,
    ModelFoundation,
    Relationship,
)

__all__ = ["PartialGroup"]


class PartialGroup(
    ModelFoundation,
    description="Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.",
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
            id="partial_group_user_id_name_unique",
            description="The combination of `user_id` and `name` must be unique.",
        ),
    ),
):
    id: Annotated[
        int,
        Declare(
            description="The unique identity of the partial group.",
            logical_type="integer",
            identity=True,
            generated=True,
        ),
    ]
    user_id: Annotated[
        int,
        Declare(
            description="Identifies the user who owns the partial group.",
            logical_type="integer",
        ),
    ]
    name: Annotated[
        str,
        Declare(description="The partial group's display name.", logical_type="string"),
    ]
    is_active: Annotated[
        bool,
        Declare(
            description="Indicates whether the partial group is active.",
            logical_type="boolean",
        ),
    ] = True
    description: Annotated[
        str | None,
        Declare(description="Describes the partial group.", logical_type="string"),
    ]
