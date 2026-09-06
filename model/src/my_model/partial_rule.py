"""The PartialRule Model."""

from decimal import Decimal
from typing import Annotated, ClassVar

from ._base import Model
from ._spec import FieldSpec, LogicalType, RelationshipSpec


class PartialRule(Model):
    """Defines an individual Partial Close rule that tells the system under which condition part of an
    open position must be closed and how much of its volume must be closed.
    """

    logical_key: ClassVar[str] = "partial_rule"
    logical_purpose: ClassVar[str] = (
        "Defines an individual Partial Close rule that tells the system under which condition part of an open "
        "position must be closed and how much of its volume must be closed."
    )
    logical_relationships: ClassVar[tuple[RelationshipSpec, ...]] = (
        RelationshipSpec(name="partial_group", type="belongs_to", target="partial_group", field="partial_group_id"),
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
            purpose="The partial rule's display name.",
        ),
    ]
    partial_group_id: Annotated[
        int,
        FieldSpec(
            type=LogicalType.integer,
            nullable=False,
            purpose="Identifies the partial group that contains the rule.",
        ),
    ]
    profit_percentage: Annotated[
        Decimal,
        FieldSpec(
            type=LogicalType.decimal,
            nullable=False,
            purpose="Defines the profit percentage that activates the rule.",
        ),
    ]
    close_percentage: Annotated[
        Decimal,
        FieldSpec(
            type=LogicalType.decimal,
            nullable=False,
            purpose="Defines the percentage of the position closed when the rule is activated.",
        ),
    ]
    status: Annotated[
        bool,
        FieldSpec(
            type=LogicalType.boolean,
            nullable=False,
            default=True,
            purpose="Indicates whether the partial rule is active.",
        ),
    ] = True
    description: Annotated[
        str | None,
        FieldSpec(
            type=LogicalType.string,
            nullable=True,
            purpose="Describes the partial rule.",
        ),
    ] = None
