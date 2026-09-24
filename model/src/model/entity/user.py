"""The User Domain Definition."""

from typing import Annotated

from model.foundation import (
    Declare,
    ModelFoundation,
    Sensitivity,
)

__all__ = ["User"]


class User(
    ModelFoundation,
    description="Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.",
    persistent="persistent",
):
    id: Annotated[
        int,
        Declare(
            description="The unique identity of the user.",
            logical_type="integer",
            identity=True,
            generated=True,
        ),
    ]
    name: Annotated[
        str,
        Declare(
            description="The user's display name.", logical_type="string", unique=True
        ),
    ]
    username: Annotated[
        str,
        Declare(
            description="The username used to identify the user.",
            logical_type="string",
            unique=True,
        ),
    ]
    password: Annotated[
        str,
        Declare(
            description="The password credential used by the user.",
            logical_type="string",
            sensitivity=Sensitivity(classification="credential", at_rest="hash"),
        ),
    ]
    api_key: Annotated[
        str,
        Declare(
            description="The API key assigned to the user.",
            logical_type="string",
            sensitivity=Sensitivity(classification="credential", at_rest="hash"),
        ),
    ]
    is_active: Annotated[
        bool,
        Declare(
            description="Indicates whether the user is active.", logical_type="boolean"
        ),
    ] = True
    description: Annotated[
        str | None, Declare(description="Describes the user.", logical_type="string")
    ]
