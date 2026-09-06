"""The TrailingRule Model."""

from decimal import Decimal
from typing import Annotated, ClassVar

from ._base import Model
from ._spec import FieldSpec, LogicalType, RelationshipSpec


class TrailingRule(Model):
    """Defines an individual rule within a Trailing Group that tells the system when and how to manage
    Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used
    to apply the required adjustments.
    """

    logical_key: ClassVar[str] = "trailing_rule"
    logical_purpose: ClassVar[str] = (
        "Defines an individual rule within a Trailing Group that tells the system when and how to manage Take "
        "Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply "
        "the required adjustments."
    )
    logical_relationships: ClassVar[tuple[RelationshipSpec, ...]] = (
        RelationshipSpec(
            name="trailing_group",
            type="belongs_to",
            target="trailing_group",
            field="trailing_group_id",
        ),
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
            purpose="The trailing rule's display name.",
        ),
    ]
    trailing_group_id: Annotated[
        int,
        FieldSpec(
            type=LogicalType.integer,
            nullable=False,
            purpose="Identifies the trailing group that contains the rule.",
        ),
    ]
    trigger_percentage: Annotated[
        Decimal,
        FieldSpec(
            type=LogicalType.decimal,
            nullable=False,
            purpose="Defines the profit percentage of the take-profit target that activates the rule.",
        ),
    ]
    take_profit_adjustment: Annotated[
        Decimal | None,
        FieldSpec(
            type=LogicalType.decimal,
            nullable=True,
            purpose="Defines the take-profit adjustment applied when the rule is activated.",
        ),
    ] = None
    stop_loss_adjustment: Annotated[
        Decimal | None,
        FieldSpec(
            type=LogicalType.decimal,
            nullable=True,
            purpose="Defines the stop-loss adjustment applied when the rule is activated.",
        ),
    ] = None
    status: Annotated[
        bool,
        FieldSpec(
            type=LogicalType.boolean,
            nullable=False,
            default=True,
            purpose="Indicates whether the trailing rule is active.",
        ),
    ] = True
    description: Annotated[
        str | None,
        FieldSpec(
            type=LogicalType.string,
            nullable=True,
            purpose="Describes the trailing rule.",
        ),
    ] = None
