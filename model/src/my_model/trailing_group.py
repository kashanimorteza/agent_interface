"""The TrailingGroup Model."""

from collections.abc import Mapping
from typing import Annotated, ClassVar

from ._base import Model
from ._spec import FieldSpec, LogicalType


class TrailingGroup(Model):
    """Defines an independent group for organizing the rules that manage Stop Loss and Take Profit
    during a trade. The group identifies the rule set, while each rule separately defines its
    activation condition and the changes to apply.
    """

    logical_key: ClassVar[str] = "trailing_group"
    logical_purpose: ClassVar[str] = (
        "Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a "
        "trade. The group identifies the rule set, while each rule separately defines its activation "
        "condition and the changes to apply."
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
            purpose="The trailing group's display name.",
        ),
    ]
    status: Annotated[
        bool,
        FieldSpec(
            type=LogicalType.boolean,
            nullable=False,
            default=True,
            purpose="Indicates whether the trailing group is active.",
        ),
    ] = True
    description: Annotated[
        str | None,
        FieldSpec(
            type=LogicalType.string,
            nullable=True,
            purpose="Describes the trailing group.",
        ),
    ] = None
