"""The Instance Domain Definition."""

from typing import Annotated

from model.entity.trading_platform import TradingPlatform
from model.entity.user import User
from model.foundation import (
    Constraint,
    Declare,
    ModelFoundation,
    Relationship,
    Sensitivity,
)

__all__ = ["Instance"]


class Instance(
    ModelFoundation,
    description="Defines a user-owned connection instance through which the system accesses a supported Trading Platform.",
    persistent="persistent",
    relationships=(
        Relationship(
            name="user",
            description="Belongs to one User through `user_id`.",
            definition=User,
            cardinality="1",
            optional=False,
        ),
        Relationship(
            name="trading_platform",
            description="Uses one Trading Platform through `trading_platform_id`.",
            definition=TradingPlatform,
            cardinality="1",
            optional=False,
        ),
    ),
    composite_constraints=(
        Constraint(
            id="instance_user_id_name_unique",
            description="The combination of `user_id` and `name` must be unique.",
        ),
    ),
):
    id: Annotated[
        int,
        Declare(
            description="The unique identity of the instance.",
            logical_type="integer",
            identity=True,
            generated=True,
        ),
    ]
    user_id: Annotated[
        int,
        Declare(
            description="Identifies the user who owns this instance.",
            logical_type="integer",
        ),
    ]
    trading_platform_id: Annotated[
        int,
        Declare(
            description="Identifies the trading platform used by this instance.",
            logical_type="integer",
        ),
    ]
    name: Annotated[
        str, Declare(description="The instance's display name.", logical_type="string")
    ]
    ip: Annotated[
        str | None,
        Declare(
            description="Identifies the technical network address used to reach the Trading Platform when required.",
            logical_type="string",
        ),
    ]
    username: Annotated[
        str | None,
        Declare(
            description="Defines the technical username used to establish the Instance connection when required.",
            logical_type="string",
        ),
    ]
    password: Annotated[
        str | None,
        Declare(
            description="Defines the technical password used to establish the Instance connection when required.",
            logical_type="string",
            sensitivity=Sensitivity(classification="credential", at_rest="encrypted"),
        ),
    ]
    api_key: Annotated[
        str | None,
        Declare(
            description="Defines the technical API credential used to establish the Instance connection when required.",
            logical_type="string",
            sensitivity=Sensitivity(classification="credential", at_rest="encrypted"),
        ),
    ]
    is_active: Annotated[
        bool,
        Declare(
            description="Indicates whether the instance is active.",
            logical_type="boolean",
        ),
    ] = True
    description: Annotated[
        str | None,
        Declare(description="Describes the instance.", logical_type="string"),
    ]
