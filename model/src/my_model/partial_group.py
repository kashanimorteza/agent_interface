"""The PartialGroup Model."""

from collections.abc import Mapping
from typing import Annotated, ClassVar

from ._base import Model
from ._spec import FieldSpec, LogicalType


class PartialGroup(Model):
    """Defines an independent group of rules for managing portions of an open trade. Its rules
    determine how much of the trade volume must be closed when profit or loss reaches specified
    thresholds.
    """

    logical_key: ClassVar[str] = "partial_group"
    logical_purpose: ClassVar[str] = (
        "Defines an independent group of rules for managing portions of an open trade. Its rules determine "
        "how much of the trade volume must be closed when profit or loss reaches specified thresholds."
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
            purpose="The partial group's display name.",
        ),
    ]
    status: Annotated[
        bool,
        FieldSpec(
            type=LogicalType.boolean,
            nullable=False,
            default=True,
            purpose="Indicates whether the partial group is active.",
        ),
    ] = True
    description: Annotated[
        str | None,
        FieldSpec(
            type=LogicalType.string,
            nullable=True,
            purpose="Describes the partial group.",
        ),
    ] = None
