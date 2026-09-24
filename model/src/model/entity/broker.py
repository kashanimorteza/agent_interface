"""The Broker Domain Definition."""

from typing import Annotated

from model.entity.user import User
from model.foundation import (
    Constraint,
    Declare,
    ModelFoundation,
    Relationship,
)

__all__ = ["Broker"]


class Broker(
    ModelFoundation,
    description="Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.",
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
            id="broker_user_id_name_unique",
            description="The combination of `user_id` and `name` must be unique.",
        ),
    ),
):
    id: Annotated[
        int,
        Declare(
            description="The unique identity of the broker.",
            logical_type="integer",
            identity=True,
            generated=True,
        ),
    ]
    name: Annotated[
        str, Declare(description="The broker's display name.", logical_type="string")
    ]
    user_id: Annotated[
        int,
        Declare(
            description="Identifies the user who owns the broker configuration.",
            logical_type="integer",
        ),
    ]
    is_active: Annotated[
        bool,
        Declare(
            description="Indicates whether the broker is active.",
            logical_type="boolean",
        ),
    ] = True
    description: Annotated[
        str | None, Declare(description="Describes the broker.", logical_type="string")
    ]
