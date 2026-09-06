"""The ActionGroup Model."""

from collections.abc import Mapping
from typing import Annotated, ClassVar

from ._base import Model
from ._spec import FieldSpec, LogicalType


class ActionGroup(Model):
    """Defines an independent grouping for trading actions based on their risk profile, such as high
    risk, normal risk, or low risk. Actions are assigned to these groups so trades can be organized
    and selected by their intended risk level.
    """

    logical_key: ClassVar[str] = "action_group"
    logical_purpose: ClassVar[str] = (
        "Defines an independent grouping for trading actions based on their risk profile, such as high risk, "
        "normal risk, or low risk. Actions are assigned to these groups so trades can be organized and "
        "selected by their intended risk level."
    )
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
            purpose="The action group's display name.",
        ),
    ]
    status: Annotated[
        bool,
        FieldSpec(
            type=LogicalType.boolean,
            nullable=False,
            default=True,
            purpose="Indicates whether the action group is active.",
        ),
    ] = True
    description: Annotated[
        str | None,
        FieldSpec(
            type=LogicalType.string,
            nullable=True,
            purpose="Describes the action group.",
        ),
    ] = None
