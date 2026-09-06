"""The User Model."""

from collections.abc import Mapping
from typing import Annotated, ClassVar

from ._base import Model
from ._spec import FieldSpec, GenerateValue, LogicalType, RuleSpec


class User(Model):
    """Defines an independent user of the system and enables multi-user operation. Each user can have a
    separate set of settings, allowing new users to be added with configurations that remain
    distinct from those of existing users.
    """

    logical_key: ClassVar[str] = "user"
    logical_purpose: ClassVar[str] = (
        "Defines an independent user of the system and enables multi-user operation. Each user can have a "
        "separate set of settings, allowing new users to be added with configurations that remain distinct "
        "from those of existing users."
    )
    logical_rules: ClassVar[tuple[RuleSpec, ...]] = (
        RuleSpec(
            rule="password is a credential and must use hash storage at rest.",
            kind="credential",
            field="password",
            storage="hash",
        ),
        RuleSpec(
            rule="api_key is a credential and must use hash storage at rest.",
            kind="credential",
            field="api_key",
            storage="hash",
        ),
    )
    logical_initial_data: ClassVar[tuple[Mapping[str, object], ...]] = (
        {
            "name": "Admin",
            "username": "admin",
            "password": GenerateValue("Generate securely"),
            "api_key": GenerateValue("Generate securely"),
        },
    )

    id: Annotated[
        int | None,
        FieldSpec(
            type=LogicalType.integer,
            nullable=False,
            auto_increment=True,
            primary_key=True,
        ),
    ] = None
    name: Annotated[
        str,
        FieldSpec(
            type=LogicalType.string,
            nullable=False,
            unique=True,
            purpose="The user's display name.",
        ),
    ]
    username: Annotated[
        str,
        FieldSpec(
            type=LogicalType.string,
            nullable=False,
            purpose="The username used to identify the user.",
        ),
    ]
    password: Annotated[
        str | None,
        FieldSpec(
            type=LogicalType.string,
            nullable=False,
            credential=True,
            purpose="The password credential used by the user.",
        ),
    ] = None
    api_key: Annotated[
        str | None,
        FieldSpec(
            type=LogicalType.string,
            nullable=False,
            credential=True,
            purpose="The API key assigned to the user.",
        ),
    ] = None
    status: Annotated[
        bool,
        FieldSpec(
            type=LogicalType.boolean,
            nullable=False,
            default=True,
            purpose="Indicates whether the user is active.",
        ),
    ] = True
    description: Annotated[
        str | None,
        FieldSpec(
            type=LogicalType.string,
            nullable=True,
            purpose="Describes the user.",
        ),
    ] = None
