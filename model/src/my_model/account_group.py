"""The AccountGroup Model."""

from collections.abc import Mapping
from typing import Annotated, ClassVar

from ._base import Model
from ._spec import FieldSpec, LogicalType


class AccountGroup(Model):
    """Defines an independent group for organizing trading accounts."""

    logical_key: ClassVar[str] = "account_group"
    logical_purpose: ClassVar[str] = "Defines an independent group for organizing trading accounts."
    logical_initial_data: ClassVar[tuple[Mapping[str, object], ...]] = (
        {"name": "Default"},
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
            purpose="The account group's display name.",
        ),
    ]
    status: Annotated[
        bool,
        FieldSpec(
            type=LogicalType.boolean,
            nullable=False,
            default=True,
            purpose="Indicates whether the account group is active.",
        ),
    ] = True
    description: Annotated[
        str | None,
        FieldSpec(
            type=LogicalType.string,
            nullable=True,
            purpose="Describes the account group.",
        ),
    ] = None
